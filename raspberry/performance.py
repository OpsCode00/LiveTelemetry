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
        f = open("infoRasp.csv", "a")
        print(str(datetime.now()) + "," + str(self.__BitSended), file=f)
        f.close()
        self.__BitSended = 0
    
    def writeSendTime(self, frame_id):
        d = open("timeSend.csv", "a")
        print(str(frame_id) + "," + str(datetime.now()), file=d)
        d.close()

    def countBitSended(self, frame_id):
        for signal in self.__telemetry_db.get_message_by_frame_id(frame_id).signals:
            self.__BitSended = self.__BitSended + signal.length