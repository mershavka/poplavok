from enums import MeasureType, timeformat
from datetime import datetime as dt, time
from typing import Optional
import json

class Series:
    def __init__(self, date=None, description: str ="", type: MeasureType = MeasureType.COMMON, id:  Optional[int] = None, measurements = None, referenceData = None):
        self.id = -1 if id is None else id
        self.date = dt.now() if date is None else date
        self.description = description
        self.type = MeasureType(type)
        self.measurements = {} if measurements is None else measurements
        self.referenceData = referenceData

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

    def getMesurementById(self, id):
        if id in self.measurements.keys():
            return self.measurements[id]
        return None

    def toJson(self):
        data = {'id': self.id, 'date': self.date.strftime(timeformat), 'type': self.type.value, 'description': self.description}        
        return data
    
    def toJsonString(self):        
        return json.dumps(self.toJson(), indent=4)
    
    def fromJson(self, jsonDict):
        self.id = int(jsonDict['id'])
        self.date = dt.strptime(jsonDict['date'], timeformat)
        self.type = MeasureType(int(jsonDict['type']))
        self.description = jsonDict['description']

    def __str__(self) -> str:
        pass