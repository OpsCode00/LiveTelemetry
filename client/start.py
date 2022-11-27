from time import sleep
import mqttSubscriber
import GUI
import threading
import performance

info = performance.Performance()
threading.Thread(GUI.GUI()).start
mqttClient = mqttSubscriber.mqttSubscriber(gui, info)
threading.Thread(info.callback()).start()