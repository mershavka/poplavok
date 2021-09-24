from enums import MeasureType, timeformat
from datetime import datetime as dt
from series import Series
from typing import Optional
import json

class Calibration:
    def __init__(self, id, series1StepId, series2StepId, date, description, models, selectedModel):
        self.id = id
        self.series1StepId = series1StepId
        self.series2StepId = series2StepId
        self.date = date
        self.description = description
        self.models = models
        self.selectedModel = selectedModel

    def toDict(self):
        data = {
            'id': self.id,
            'series1StepId': self.series1StepId,
            'series2StepId': self.series2StepId,
            'date': self.date.strftime(timeformat),
            'description': self.description
        }
        return data

    def toJsonString(self):
        return json.dumps(self.toDict(), indent=4)

    
    def fromJson(self, jsonDict):
        self.id = int(jsonDict['id'])
        self.date = dt.strptime(jsonDict['date'], timeformat)
        self.type = MeasureType(int(jsonDict['type']))
        self.description = jsonDict['description']
