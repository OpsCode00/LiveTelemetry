import cantools
import tkinter
from PIL import ImageTk, Image
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import randint, seed


class GUI:
    def __init__(self) -> None:

        self.__root = tkinter.Tk()
        print("Creating Tkinter instance..\n")
        self.__root.geometry("850x600")
        print("Initialize canvas..\n")
        self.__root.title("UniprRacingTeam LiveTelemetry")
        print("Initialize title..\n")
        self.__root.iconbitmap("Logo_UniPR_Racing_Team.ico")
        print("Initialize icon..\n")
        self.__root.resizable(False, False)

        self.__MAX_DATA = 50
        self.__signalNameDict = {}
        self.__signalValueDict = {}
        self.__graphList = ["BrakeFront", "BrakeRear", "APPS1", "APPS2", "SOC", "BatteryVoltage"]
        print("Dictionary created..\n")

        self.__telemetry_db = cantools.database.load_file('Telemetry.dbc')
        print("Database loaded..\n")

        # Ciclo per popolare i dizionari di label contenente il nome del messasggio e per quelle contenenti il valore del segnale
        for message in self.__telemetry_db.messages:
            # signalList ad ogni ciclo contiene i segnali nel messaggio corrente
            signalList = self.__telemetry_db.get_message_by_name(str(message.name)).signals
            for signal in signalList:
                if signal.name in self.__graphList:
                    self.__signalValueDict[signal.name] = tkinter.Label(self.__root, text="0", bg="#adb5bd", fg="black", font=("Arial", 12), width=8)
                    self.__signalNameDict[signal.name] = tkinter.Label(self.__root, text=str(signal.name), fg="black", font=("Arial", 12), cursor="hand2")                
                else:
                    # dizionario signalName -> Label inizializzata a zero che conterrà il valore del segnale
                    self.__signalValueDict[signal.name] = tkinter.Label(self.__root, text="0", bg="#adb5bd", fg="black", font=("Arial", 12), width=8)
                    # dizionario signalName -> Label con testo uguale a signalName
                    self.__signalNameDict[signal.name] = tkinter.Label(self.__root, text=str(signal.name), fg="black", font=("Arial", 12))
        
        print("Dictionary populated..\n")


        print("Creating GUI..\n")
        self.__img = ImageTk.PhotoImage(Image.open("Logo_UniPR_Racing_Team.png").resize([207,120]))
        self.__logo = tkinter.Label(self.__root, image = self.__img)
        self.__logo.place(x=20, y=50)
        self.__title1 = tkinter.Label(self.__root, text="Live Telemetry", fg="black", font=("Arial", 28))
        self.__title1.place(x=250, y=90)
        self.__title2 = tkinter.Label(self.__root, text="Client", fg="black", font=("Arial", 28))
        self.__title2.place(x=320, y=130)

        self.__batteryPanel = tkinter.Label(self.__root, text="Battery", fg="black", font=("Arial", 14))
        self.__batteryPanel.place(x=670, y=330)
        self.__signalNameDict["BatteryVoltage"].place(x=586, y=370)
        self.__signalValueDict["BatteryVoltage"].place(x=735, y=370)
        self.__signalNameDict["SOC"].place(x=623, y=405)
        self.__signalNameDict["SOC"].bind("<Button-1>", lambda e: GUI.plotGraph(self, "SOC"))
        self.__signalValueDict["SOC"].place(x=735, y=405)
        self.__signalNameDict["CellMaxVoltage"].place(x=586, y=440)
        self.__signalValueDict["CellMaxVoltage"].place(x=735, y=440)
        self.__signalNameDict["CellMinVoltage"].place(x=586, y=475)
        self.__signalValueDict["CellMinVoltage"].place(x=735, y=475)
        self.__signalNameDict["CellMaxTemp"].place(x=590, y=510)
        self.__signalValueDict["CellMaxTemp"].place(x=735, y=510)
        self.__signalNameDict["CellMeanTemp"].place(x=586, y=545)
        self.__signalValueDict["CellMeanTemp"].place(x=735, y=545)

        self.__tempMotorInverterPanel = tkinter.Label(self.__root, text="Motor & Inverter Temp", fg="black", font=("Arial", 14))
        self.__tempMotorInverterPanel.place(x=605, y=120)
        self.__signalNameDict["TempInvLeft"].place(x=586, y=160)
        self.__signalValueDict["TempInvLeft"].place(x=735, y=160)
        self.__signalNameDict["TempInvRight"].place(x=586, y=195)
        self.__signalValueDict["TempInvRight"].place(x=735, y=195)
        self.__signalNameDict["TempMotorLeft"].place(x=586, y=230)
        self.__signalValueDict["TempMotorLeft"].place(x=735, y=230)
        self.__signalNameDict["TempMotorRight"].place(x=586, y=265)
        self.__signalValueDict["TempMotorRight"].place(x=735, y=265)

        self.__pedalPanel = tkinter.Label(self.__root, text="Pedals", fg="black", font=("Arial", 14))
        self.__pedalPanel.place(x=410, y=365)
        self.__signalNameDict["BrakeFront"].place(x=350, y=405)
        self.__signalNameDict["BrakeFront"].bind("<Button-1>", lambda e: GUI.plotGraph(self, "BrakeFront"))
        self.__signalValueDict["BrakeFront"].place(x=460, y=405)
        self.__signalNameDict["BrakeRear"].place(x=350, y=440)
        self.__signalNameDict["BrakeRear"].bind("<Button-1>", lambda e: GUI.plotGraph(self, "BrakeRear"))
        self.__signalValueDict["BrakeRear"].place(x=460, y=440)
        self.__signalNameDict["Steering"].place(x=350, y=475)
        self.__signalValueDict["Steering"].place(x=460, y=475)
        self.__signalNameDict["APPS2"].place(x=350, y=510)
        self.__signalNameDict["APPS2"].bind("<Button-1>", lambda e: GUI.plotGraph(self, "APPS2"))
        self.__signalValueDict["APPS2"].place(x=460, y=510)
        self.__signalNameDict["APPS1"].place(x=350, y=545)
        self.__signalNameDict["APPS1"].bind("<Button-1>", lambda e: GUI.plotGraph(self, "APPS1"))
        self.__signalValueDict["APPS1"].place(x=460, y=545)

        self.__infoPanel = tkinter.Label(self.__root, text="Info", fg="black", font=("Arial", 14))
        self.__infoPanel.place(x=170, y=260)
        self.__signalNameDict["VehicleSpeed"].place(x=68, y=300)
        self.__signalValueDict["VehicleSpeed"].place(x=220, y=300)
        self.__signalNameDict["Map"].place(x=105, y=335)
        self.__signalValueDict["Map"].place(x=220, y=335)
        self.__signalNameDict["TcMap"].place(x=95, y=370)
        self.__signalValueDict["TcMap"].place(x=220, y=370)
        self.__signalNameDict["TractionEnable"].place(x=65, y=405)
        self.__signalValueDict["TractionEnable"].place(x=220, y=405)
        self.__signalNameDict["TorqueVectoringEnable"].place(x=30, y=440)
        self.__signalValueDict["TorqueVectoringEnable"].place(x=220, y=440)
        self.__signalNameDict["MaxPower"].place(x=75, y=475)
        self.__signalValueDict["MaxPower"].place(x=220, y=475)
        self.__signalNameDict["MaxTorque"].place(x=75, y=510)
        self.__signalValueDict["MaxTorque"].place(x=220, y=510)
        self.__signalNameDict["MaxRegen"].place(x=75, y=545)
        self.__signalValueDict["MaxRegen"].place(x=220, y=545)
        print("GUI created..\n")

        self.__root.mainloop()
        print("GUI started..\n")

    def updateGUI(self, signalName, value):
        self.__signalValueDict[signalName]["text"] = value

    def plotGraph(self, signalName):
        fig = plt.figure()
        plt.get_current_fig_manager().set_window_title(signalName)
        plt.get_current_fig_manager().window.wm_iconbitmap("Logo_UniPR_Racing_Team.ico")
        ax = fig.add_subplot(1, 1, 1)
        xs = []
        ys = []
        ani = animation.FuncAnimation(fig, GUI.animateGraph, fargs=(self, xs, ys, ax, signalName), interval=1000)
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.20)
        plt.title(signalName)
        plt.ylabel(signalName)
        plt.show()

    def animateGraph(i, self, xs, ys, ax, signalName):
        # Read temperature (Celsius) from TMP102
        temp_c = float(self.__signalValueDict[signalName]["text"])
        print(temp_c)
        # Add x and y to lists
        xs.append(dt.datetime.now().strftime('%H:%M:%S'))
        ys.append(temp_c)

        # Limit x and y lists to 20 items
        xs = xs[-self.__MAX_DATA:]
        ys = ys[-self.__MAX_DATA:]

        # Draw x and y lists
        ax.clear()
        ax.plot(xs, ys)

        #format plot
        plt.xticks(rotation=65, ha='right')
        plt.subplots_adjust(bottom=0.20)
        plt.title(signalName)
        plt.ylabel(signalName)