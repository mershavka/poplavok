from enums import MeasureType, timeformat
from datetime import datetime as dt
from series import Series
from typing import Optional
import json

class Measurement:
    def __new__(cls, seriesId, duration, periodicity, date, description: str ="", type: MeasureType = MeasureType.COMMON, id:  Optional[int] = None, calibrationId:  Optional[int] = None):
        if seriesId is None:
            return None
        instance = super().__new__(cls)
        return instance

    def __init__(self, seriesId, duration, periodicity, date, description: str ="", type=MeasureType.COMMON, id:  Optional[int] = None, calibrationId:  Optional[int] = None):
        if seriesId is None:
            pass
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
        return json.dumps(data, indent=4)

    def __str__(self) -> str:
        pass