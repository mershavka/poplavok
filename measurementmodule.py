from threading import Thread, Event
import time
from measurement import Measurement


class MeasurementModule:

    def __init__(self) -> None:
        self.stopEvent = Event()
        self.th = None
        self.readFunc = None
        self.writeFunc = None

    def setReadFunc(self, f):
        self.readFunc = f

    def setWriteFunc(self, f):
        self.writeFunc = f

    def __measurementsThreadFunc(self, duration, periodicity):
        expStart = time.time()
        timing = 0
        while time.time() - expStart <= duration:
            if self.stopEvent.is_set():
                break
            if time.time() - timing >= periodicity:
                timing = time.time()
                dataDictionary = self.readFunc()
                print(dataDictionary)
                self.writeFunc(dataDictionary)

    def stopMeasurement(self):
        if self.th.is_alive():
            self.stopEvent.set()
        
    def startMeasurement(self, m : Measurement):
        if self.readFunc is None or self.writeFunc is None:
            return
        duration = m.duration
        period = m.periodicity
        self.th = Thread(target=MeasurementModule.__measurementsThreadFunc, args=(duration, period))
        self.stopEvent.clear()
        self.th.start()
