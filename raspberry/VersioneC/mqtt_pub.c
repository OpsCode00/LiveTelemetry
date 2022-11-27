#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mosquitto.h>
#include <canlib.h>
#include <pthread.h>

typedef struct structCanMessage canMessage;
typedef struct structCanMessage 
{
	long id;
	unsigned char data[8];
	unsigned int dlc;
	unsigned int flags;
	unsigned long timestamp;
} structCanMessage;

typedef struct structThreadArguments argThread;
typedef struct structThreadArguments
{
	canMessage message;
	struct mosquitto * mosq;
} structThreadArguments;


void Check(const char* id, canStatus stat){//funzione che serve per controllare gli errori della libreria canlib, (ovviamente palesemetne copiata dall'esempio su internet)
  if (stat != canOK) {
    char buf[50];
    buf[0] = '\0';
    canGetErrorText(stat, buf, sizeof(buf));
    printf("%s: failed, stat=%d (%s)\n", id, (int)stat, buf);
    exit(1);
  }
}

void publishMessage(argThread *arguments){
	//inizializzo due array temporanei dove andare a salvare le stringhe che mi serviranno per il topic e il payload
	char topic[9];
	char payload[4];
	for(int i=0;i<8;++i){
		sprintf(topic, "%d/%d", arguments->message.id, i);//la sezione madre sarà l'ID.... e poi ci saranno 7 sottosezioni con i valori dei singoli bytes (quindi sto trasformanto i vari valori in una stringa)
		sprintf(payload,"%d", arguments->message.data[i]);//il payload sarà il valore del singolo byte in decimale (anche qui sto trasformando un intero in una stringa)
		//printf("%s", payload);
		mosquitto_publish(mosq, NULL, topic , strlen(payload), payload, 0, false);
	}	
}

/* void publishMessage(long id, char data[], struct mosquitto *mosq){
	char topic[9];
	char payload[4];
	for(int i=0;i<8;++i){
		sprintf(topic, "%d/%d", id, i);//la sezione madre sarà l'ID.... e poi ci saranno 7 sottosezioni con i valori dei singoli bytes
		sprintf(payload,"%d", data[i]);
		//printf("%s", payload);
		mosquitto_publish(mosq, NULL, topic , strlen(payload), payload, 0, false);
	}
} */

void readMessagesLoop(canHandle hcan, int canChannel, struct mosquitto *mosq){
	canStatus stat = canOK;//struct per controllora l'andata a buon fine di ogni operazione
	canMessage message;
	pthread_t publishThread;
	argThread threadArguments;
	threadArguments.mosq = mosq;
	while(1) {
		stat = canReadWait(hcan, &message.id, message.data, &message.dlc, &message.flags, &message.timestamp, 500);
		printf("Id: %ld, Msg: %u %u %u %u %u %u %u %u length: %u Flags: %lu\n",message.id, message.dlc, message.data[0], message.data[1], message.data[2], message.data[3], message.data[4], message.data[5], message.data[6], message.data[7], message.timestamp);
		threadArguments.message = message;
		//publishMessage(message.id, message.data, mosq);
		//creo il thread, passandogli una struct contenente tutti i dati necessari alla funzione di publish
		//(il messaggio ed il puntatore a struct per la libreria mosquitto)
		pthread_create(&publishThread, NULL, publishMessage, *threadArguments);
	}
}


int main(){
	int rc;
	struct mosquitto * mosq;
	//inizializzazione e connessione

	mosquitto_lib_init();
	canInitializeLibrary();

	mosq = mosquitto_new("publisher-test", true, NULL);

	rc = mosquitto_connect(mosq, "localhost", 1883, 60);
	if(rc != 0){
		printf("Connessione al broker fallita! Codice d'errore: %d\n", rc);
		mosquitto_destroy(mosq);
		return -1;
	}
	printf("Connesso al broker!\n");
	//inizializzazione can

	canStatus stat = canOK;
	CanHandle hcan;
	hcan = canOpenChannel(0, canOPEN_ACCEPT_VIRTUAL); //accetto tutti i canali can0..... compreso vcan0
	if(hcan < 0)
		Check("canOpenChannel", (canStatus)hcan);

	kvBusParamsTq params = {8, 2, 2, 1, 3, 20}; //settaggi molto specifici per il settaggio dei parametri del nostro logkvaser (500kbit/s)
	stat = canSetBusParamsTq(hcan, params);
	Check("canSetBusParams", stat);

	stat = canBusOn(hcan);
  	Check("canBusOn", stat);
	//lettura e publish

	readMessagesLoop(hcan, 0, mosq);//inizio un ciclo infinito dove leggo ed invio i messagi letti dal can
	/*
	canMessage message;
	message.id = 150;
	for(int i=0;i<8;++i)
		message.data[i]=i;
	message.dlc = 8;
	message.timestamp = 180;
	message.flags = 0;
	char topic[9];
	char payload[4];
	for(int i=0;i<8;++i){
		sprintf(topic, "%d/%d",message.id, i);
		sprintf(payload,"%d", message.data[i]);
		printf("%s", payload);
		mosquitto_publish(mosq, NULL, topic , strlen(payload), payload, 0, false);
	}
	*/
	mosquitto_disconnect(mosq);
	mosquitto_destroy(mosq);
	mosquitto_lib_cleanup();
	return 0;
}
