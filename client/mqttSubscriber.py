import threading
from tkinter import Label
import paho.mqtt.client as mqtt
import cantools
import performance

class mqttSubscriber():
    def __init__(self, gui, performance) -> None:
        
        print("\nMQTT Starting..")

        self.__GUI = gui

        #Client MQTT Istance
        self.__MQTT_client = mqtt.Client()
        self.__MQTT_client.on_connect = self.on_connect
        self.__MQTT_client.on_message = self.on_message
        print("\nCreating Istance..")

        #Connect to broker (address: localhost, port:1883 default)
        self.__MQTT_client.connect("localhost", 1883)
        print("\nConnecting to Broker..")

        self.__MQTT_client.subscribe("UniprRacingTeam/+/+", 0)
        print("\nSubscribing to UniprRacingTeam topic")

        self.__MQTT_client.loop_start()
        print("\nMQTT loop started..")

        #Variables
        self.__info = performance

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

    # Callback triggerata quando un messaggio viene ricevuto nel topic a cui sono sottoscritto
    def on_message(self, client, userdata, message):
        value = round(float(message.payload.decode("utf-8")), 2)
        topic = str(message.topic)
        threading.Thread(self.__info.writeSendTime(topic.split("/")[1])).start()
        threading.Thread(self.__GUI.updateGUI(topic.split("/")[2], value)).start()
        self.__info.countBitSended(topic) #Non so se ha senso chiamare questa funzione in un thread
        #signal_label_dic[signal_name]["text"] = str(value)