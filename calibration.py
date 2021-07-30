from enums import MeasureType, timeformat
from datetime import datetime as dt
from series import Series
from typing import Optional
import json

class Calibration:
    def __init__(self, id, series1StepId, series2StepId, date, description):
        self.id = id
        self.series1StepId = series1StepId
        self.series2StepId = series2StepId
        self.date = date
        self.description = description
        # self.selectedModel1 = 
        # self.selectedModel2 = 

    def calculateCH4(self, dataDict):
        

    def toJson(self):
        data = {'id': self.id, 'series1StepId': self.series1StepId, 'series2StepId': self.series2StepId,'date': self.date.strftime(timeformat), 'description': self.description}
        return json.dumps(data, indent=4)