from enums import MeasureType
from datetime import datetime as dt
from typing import Optional
import json

class Series:
    timeformat = "%Y%m%d%H%M%S"
    def __init__(self, date=None, description: str ="", type: MeasureType = MeasureType.COMMON, id:  Optional[int] = None, measurements = None):
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

    def getMeasurementsDict(self):
        return self.measurements

    def getMeasurementsList(self):
        return [i for i in self.measurements.values()]

    def getMeasurementsIds(self):
        return [i for i in self.measurements.keys()]

    def toJson(self):
        data = {'id': self.id, 'date': self.date.strftime(Series.timeformat), 'type': self.type.value, 'description': self.description}
        return json.dumps(data, indent=4)

    def __str__(self) -> str:
        pass