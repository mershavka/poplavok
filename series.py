from enums import MeasureType
from datetime import datetime as dt
from typing import Optional

class Series:

    def __init__(self, date=None, description: str ="", type=MeasureType.COMMON, id:  Optional[int] = None, measurements = None):
        self.id = -1 if id is None else id
        self.date = dt.now() if date is None else date
        self.description = description
        self.type = type
        self.measurements = {} if measurements is None else measurements

    def setId(self, id):
        self.id = id

    def updateDescription(self, newDescription: str):
        self.description = newDescription

    def addMeasurement(self, id, measurement):
        if id not in self.measurements.keys():
            self.measurements[id] = measurement
        return self.measurements[id]

    def popMeasurement(self, id):
        if id in self.measurements.keys():
            return self.measurements.pop(id)
        else:
            return None

    def __str__(self) -> str:
        pass