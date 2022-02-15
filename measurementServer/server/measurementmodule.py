from ..common import Measurement
from .msLogger import MsLogger

from threading import Thread, Event
import time


class MeasurementModule:

    def __init__(self) -> None:
        self.stopEvent = Event()
        self.th = None
        self.readFunc = None
        self.writeFunc = None
        self.stopFunc = None
        self.logger = MsLogger().get_logger()
        self.logger.info("MeasurementModule initialized")

    def setReadFunc(self, f):
        self.readFunc = f

    def setWriteFunc(self, f):
        self.writeFunc = f

    def setStopFunc(self, f):
        self.stopFunc = f

    def __measurementsThreadFunc(self, duration, periodicity):
        expStart = time.time()
        timing = 0
        while time.time() - expStart <= duration:
            if self.stopEvent.is_set():
                break
            if time.time() - timing >= periodicity:
                timing = time.time()
                dataDictionary = self.readFunc()
                self.logger.info(str(dataDictionary))
                self.writeFunc(dataDictionary)
        self.stopFunc()

    def stopMeasurement(self):
        if not self.th is None:
            if self.th.is_alive():
                self.logger.info("Measurement stopped")
                self.stopEvent.set()
        
    def startMeasurement(self, m : Measurement):
        if self.readFunc is None or self.writeFunc is None:
            return
        duration = m.duration
        period = m.periodicity
        self.th = Thread(target=MeasurementModule.__measurementsThreadFunc, args=(self, duration, period))
        self.stopEvent.clear()
        self.th.start()
        self.logger.info("Measurement started")
    
    def isWorking(self):
        if self.th is None:
            return False
        return self.th.is_alive()
