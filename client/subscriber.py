import threading
import paho.mqtt.client as mqtt
import cantools
import tkinter as tk
from tkinter import Entry, Label, ttk
import performance
from PIL import ImageTk, Image
import webbrowser
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

connected = False
messageRecieved = False

broker_address = "localhost"
port = 1883

#--------------------------------------------------- Inizializzazione GUI --------------------------------------------------#

root = tk.Tk()
frame = root.geometry("850x600")
root.title("UniprRacingTeam LiveTelemetry")

#---------------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------- Creazione dizionario di Label ---------------------------------------------#
signalValueDict = {}
label_dic = {}
graph_list = ["BrakeFront", "BrakeRear", "APPS1", "APPS2", "SOC", "BatteryVoltage"]
db = cantools.database.load_file("client\Telemetry.dbc")

# Ciclo per popolare i dizionari di label contenente il nome del messasggio e per quelle contenenti il valore del segnale
for message in db.messages:
    # signalList ad ogni ciclo contiene i segnali nel messaggio corrente
    signalList = db.get_message_by_name(str(message.name)).signals
    for signal in signalList:
        if signal.name in graph_list:
            signalValueDict[signal.name] = Label(root, text="0", bg="#adb5bd", fg="black", font=("Arial", 12), width=8)
            label_dic[signal.name] = Label(root, text=str(signal.name), fg="black", font=("Arial", 12), cursor="hand2")
        else:
            # dizionario signalName -> Label inizializzata a zero che conterrà il valore del segnale
            signalValueDict[signal.name] = Label(root, text="0", bg="#adb5bd", fg="black", font=("Arial", 12), width=8)
            # dizionario signalName -> Label con testo uguale a signalName
            label_dic[signal.name] = Label(root, text=str(signal.name), fg="black", font=("Arial", 12))


#---------------------------------------------------------------------------------------------------------------------------#

# Callback triggerata quando viene chiamata la funzione .connect()
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Client is connected")
        global connected
        connected = True
    else:
        print("Client is not connected")

# Callback triggerata quando un messaggio viene ricevuto nel topic a cui sono sottoscritto
def on_message(client, userdata, message):
    topic = str(message.topic)
    threading.Thread(info.writeSendTime(topic.split("/")[1])).start()
    info.countBitSended(topic)
    global messageRecieved
    messageRecieved = True
    value = message.payload.decode("utf-8")
    value = round(float(value), 2)
    print("Message recieved : " + str(value))
    print("Topic" + str(message.topic))
    signal_name = topic.split("/")[2]
    signalValueDict[signal_name]["text"] = str(value)

def brakeFrontGraph():
    fig = plt.figure()
    plt.show()

# inizializzazione istanza client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port)
info = performance.Performance()

img = ImageTk.PhotoImage(Image.open("Logo_UniPR_Racing_Team.png").resize([207,120]))
logo = Label(root, image = img)
logo.place(x=20, y=50)
title1 = Label(root, text="Live Telemetry", fg="black", font=("Arial", 28))
title1.place(x=250, y=90)
title2 = Label(root, text="Client", fg="black", font=("Arial", 28))
title2.place(x=320, y=130)

BatteryPanel = Label(root, text="Battery", fg="black", font=("Arial", 14))
BatteryPanel.place(x=670, y=330)
label_dic["BatteryVoltage"].place(x=586, y=370)
signalValueDict["BatteryVoltage"].place(x=735, y=370)
label_dic["SOC"].place(x=623, y=405)
label_dic["SOC"].bind("<Button-1>", lambda e: brakeFrontGraph())
signalValueDict["SOC"].place(x=735, y=405)
label_dic["CellMaxVoltage"].place(x=586, y=440)
signalValueDict["CellMaxVoltage"].place(x=735, y=440)
label_dic["CellMinVoltage"].place(x=586, y=475)
signalValueDict["CellMinVoltage"].place(x=735, y=475)
label_dic["CellMaxTemp"].place(x=590, y=510)
signalValueDict["CellMaxTemp"].place(x=735, y=510)
label_dic["CellMeanTemp"].place(x=586, y=545)
signalValueDict["CellMeanTemp"].place(x=735, y=545)

TempMotorInverterPanel = Label(root, text="Motor & Inverter Temp", fg="black", font=("Arial", 14))
TempMotorInverterPanel.place(x=605, y=120)
label_dic["TempInvLeft"].place(x=595, y=160)
signalValueDict["TempInvLeft"].place(x=735, y=160)
label_dic["TempInvRight"].place(x=592, y=195)
signalValueDict["TempInvRight"].place(x=735, y=195)
label_dic["TempMotorLeft"].place(x=586, y=230)
signalValueDict["TempMotorLeft"].place(x=735, y=230)
label_dic["TempMotorRight"].place(x=586, y=265)
signalValueDict["TempMotorRight"].place(x=735, y=265)

PedalPanel = Label(root, text="Pedals", fg="black", font=("Arial", 14))
PedalPanel.place(x=410, y=365)
label_dic["BrakeFront"].place(x=350, y=405)
label_dic["BrakeFront"].bind("<Button-1>", lambda e: brakeFrontGraph())
signalValueDict["BrakeFront"].place(x=460, y=405)
label_dic["BrakeRear"].place(x=350, y=440)
label_dic["BrakeRear"].bind("<Button-1>", lambda e: brakeFrontGraph())
signalValueDict["BrakeRear"].place(x=460, y=440)
label_dic["Steering"].place(x=350, y=475)
signalValueDict["Steering"].place(x=460, y=475)
label_dic["APPS2"].place(x=350, y=510)
label_dic["APPS2"].bind("<Button-1>", lambda e: brakeFrontGraph())
signalValueDict["APPS2"].place(x=460, y=510)
label_dic["APPS1"].place(x=350, y=545)
label_dic["APPS1"].bind("<Button-1>", lambda e: brakeFrontGraph())
signalValueDict["APPS1"].place(x=460, y=545)

InfoPanel = Label(root, text="Info", fg="black", font=("Arial", 14))
InfoPanel.place(x=170, y=260)
label_dic["VehicleSpeed"].place(x=68, y=300)
signalValueDict["VehicleSpeed"].place(x=220, y=300)
label_dic["Map"].place(x=105, y=335)
signalValueDict["Map"].place(x=220, y=335)
label_dic["TcMap"].place(x=95, y=370)
signalValueDict["TcMap"].place(x=220, y=370)
label_dic["TractionEnable"].place(x=65, y=405)
signalValueDict["TractionEnable"].place(x=220, y=405)
label_dic["TorqueVectoringEnable"].place(x=30, y=440)
signalValueDict["TorqueVectoringEnable"].place(x=220, y=440)
label_dic["MaxPower"].place(x=75, y=475)
signalValueDict["MaxPower"].place(x=220, y=475)
label_dic["MaxTorque"].place(x=75, y=510)
signalValueDict["MaxTorque"].place(x=220, y=510)
label_dic["MaxRegen"].place(x=75, y=545)
signalValueDict["MaxRegen"].place(x=220, y=545)

# subscribe a tutti i topic sotto UniprRacingTeam
client.subscribe("UniprRacingTeam/+/+", 0)
threading.Thread(info.callback()).start()

client.loop_start()
root.mainloop()