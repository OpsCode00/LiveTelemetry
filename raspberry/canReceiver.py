import cantools
import can
import threading
import os
import traceback

class CanReceiver(can.Listener):
    """
    """
    def __init__(self, telemetry_db, mqttClient, infoPerformance) -> None:
        """
        """
        print("\nCAN Starting..")

        #Lettura database
        self.__telemetry_db = cantools.database.load_file(telemetry_db)
        print("\nDBC Loaded..")

        #Inizializzazione canali CAN bus
        #self.__can_disable()
        #self.__can_enable()
        print("\nCan enabled")

        #Inizializzazione interfacce CAN bus
        self.__can0_bus = can.interface.Bus("can0", bustype="socketcan")
        #self.__can0_bus = can.interface.Bus("can1", bustype="socketcan")

        #Per ricevere tutti i messaggi
        can.Notifier(self.__can0_bus, [self])
        #can.Notifier(self.__can1_bus, [self])

        #Inizializzazione dizionario messaggi letti
        self.__dict_message = {}

        #VARIABLES
        #Inizializzazione lista id
        self.__messages_id_list = []

        #Istanza MQTT
        self.__mqtt = mqttClient
        print("\nInit MQTT class..")

        self.__info = infoPerformance

        for message in self.__telemetry_db.messages:
            self.__messages_id_list.append(message.frame_id)

        print(self.__messages_id_list)

    def on_message_received(self, message):
            """
            Callback chiamata alla ricezione di un nuovo messaggio sul CAN bus
            message: Messaggio ricevuto
            """
            message_id = message.arbitration_id

            try:
                if message_id in self.__messages_id_list:
                    self.__dict_message[message_id] = self.__telemetry_db.decode_message(message_id, message.data)
                    self.__info.countBitSended(message_id)
                    for signalName in self.__dict_message[message_id]:
                        topic = "UniprRacingTeam/" + str(self.__telemetry_db.get_message_by_frame_id(message_id).name) + "/" + str(signalName)
                        self.__mqtt.publishMessage(topic, self.__dict_message[message_id][signalName])
                        threading.Thread(self.__info.writeSendTime(message_id)).start()
            except:
                print("Publish error!!")
                print(traceback.format_exc())  

    def __can_enable(self):
        """
        Attivazione del canale can0
        """
        os.system("sudo ip link set can0 up type can bitrate 250000")

    def __can_disable(self):
        """
        Disattivazione del canale can0
        """
        os.system("sudo ip link set can0 down")

    def get_dict_message(self):
        return self.__dict_message

    def get_db(self):
        return self.__telemetry_db
