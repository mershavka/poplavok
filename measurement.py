from enums import MeasureType, timeformat
from datetime import datetime as dt
from series import Series
from typing import Optional
import json

class Measurement:
    def __new__(cls, *args, **kwargs):
        # if kwargs.get("seriesId", None) is None:
        #     return None
        instance = super().__new__(cls)
        return instance

    def __init__(self, seriesId=None, duration=None, periodicity=None, date=None, description: str ="", type=MeasureType.COMMON, id:  Optional[int] = None, calibrationId:  Optional[int] = None):
        self.seriesId = seriesId
        self.duration = duration
        self.periodicity = periodicity
        self.date = dt.now() if date is None else date
        self.description = description
        self.type = type
        self.id = -1 if id is None else id
        self.calibrationId = calibrationId

    def setId(self, id):
        self.id = id

    def toJson(self):
        data = {'id': self.id, 'seriesId': self.seriesId, 'calibrationId': self.calibrationId,'date': self.date.strftime(timeformat), 'type': self.type.value, 'duration': self.duration, 'periodicity': self.periodicity,'description': self.description}
        return data
    
    def toJsonString(self):
        return json.dumps(self.toJson(), indent=4)

    def fromJson(self, jsonDict):
        self.id = int(jsonDict["id"])
        self.seriesId = int(jsonDict["seriesId"])
        self.calibrationId = int(jsonDict["calibrationId"])
        self.date = dt.strptime(jsonDict["date"], timeformat)
        self.type = MeasureType(int(jsonDict["type"]))
        self.duration = float(jsonDict["duration"])
        self.periodicity = float(jsonDict["periodicity"])
        self.description = jsonDict["description"]

    def __str__(self) -> str:
        pass