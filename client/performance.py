from asyncio import sleep
import cantools
from datetime import datetime
import repeatedTimer

class Performance():
    """
    Costruttore della classe
    """
    def __init__(self) -> None:
        
        self.__telemetry_db = cantools.database.load_file("Telemetry.dbc")

        self.__BitSended = 0

    def callback(self):
        repeatedTimer.RepeatedTimer(1, self.writeBitrate)

    def writeBitrate(self):
        f = open("infoClient.csv", "a")
        print(str(datetime.now()) + "," + str(self.__BitSended), file=f)
        f.close()
        self.__BitSended = 0
    
    def writeSendTime(self, frame_name):
        d = open("timeSend.csv", "a")
        print(str(frame_name) + "," + str(datetime.now()), file=d)
        d.close()

    def countBitSended(self, topic):
        for signal in self.__telemetry_db.get_message_by_name(topic.split("/")[1]).signals:
            if signal.name == topic.split("/")[2]:
                self.__BitSended = self.__BitSended + signal.length