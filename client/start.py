import mqttSubscriber
import GUI
import threading
import performance

info = performance.Performance()
gui = GUI.GUI()
mqttClient = mqttSubscriber.mqttSubscriber(gui, info)
threading.Thread(info.callback()).start()