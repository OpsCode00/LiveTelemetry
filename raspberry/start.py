import canReceiver
import mqttPublisher
import performance
import threading

#mqttClient = mqttPublisher.mqttPublisher()
mqttThread = threading.Thread(mqttPublisher.mqttPublisher())
mqttThread.start()
mqttClient = mqttThread.join()
#info = performance.Performance()
infoThread = threading.Thread(performance.Performance())
infoThread.start()
info = infoThread.join()
#receiver = canReceiver.CanReceiver("Telemetry.dbc", mqttClient, info)
receiverThread = threading.Thread(canReceiver.CanReceiver, args=("Telemetry.dbc", mqttClient, info))
receiverThread.start()
receiver = receiverThread.join()
threading.Thread(info.callback(), daemon=True).start()