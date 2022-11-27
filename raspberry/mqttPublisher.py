import paho.mqtt.client as mqtt

class mqttPublisher():
    """
    Costruttore della classe
    """
    def __init__(self) -> None:

        print("\nMQTT Client Starting..")

        #Istanza Client MQTT
        self.__MQTT_client = mqtt.Client()
        self.__MQTT_client.on_connect = self.on_connect
        print("\nCreating Istance..")

        #Collegamento al broker (indirizzo localhost, porta 1883 default)
        self.__MQTT_client.connect("100.88.213.64", 1883)
        print("\nConnecting to Broker..")

        self.__MQTT_client.loop_start()
        print("\nMQTT loop started..")

    """
    Callback chiamata quando il broker risponde alla .connect()
    client: the client instance for this callback
    userdata: the private user data as set in Client() or user_data_set()
    flags: response flags sent by the broker
    rc: the connection result
    0: Connection successful
    1: Connection refused - incorrect protocol version
    2: Connection refused - invalid client identifier
    3: Connection refused - server unavailable
    4: Connection refused - bad username or password
    5: Connection refused - not authorised
    6-255: Currently unused.
    """
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("\nClient connected..")
        elif rc==3:
            print("\nSever unavailable..")
        else:
            print("\nClient not connected..")
    
    """
    """
    def publishMessage(self, topic:str, message_data): 
        self.__MQTT_client.publish(topic, message_data, 0, False)
        

