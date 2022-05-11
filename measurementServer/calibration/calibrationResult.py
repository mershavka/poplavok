from ..common import ValuesNames, timeformat
from .calibrationModel import CalibrationModel
from .calibrationFunctions import RsR0_calc

from operator import index
from datetime import datetime as dt
from typing import Optional
import json

class CalibrationResult:
    
    def __init__(self, id:  Optional[int] = None, series1Ids :  Optional[list] = None, series2Ids:  Optional[list] = None, date=None, V0Model : Optional[CalibrationModel] = None, CH4Model : Optional[CalibrationModel] = None, CH4LRModel : Optional[CalibrationModel] = None) -> None:
        self.id = id
        self.series1Ids = series1Ids
        self.series2Ids = series2Ids

        self.date = date

        self.V0Model = V0Model
        self.CH4Model = CH4Model
        self.CH4LRModel = CH4LRModel

    def calculateCH4(self, dataDict):
        dataDict[ValuesNames.voltage0.name] = self.V0Model.calculate(dataDict)
        dataDict[ValuesNames.rsr0.name] = RsR0_calc(dataDict)
        dataDict[ValuesNames.ch4.name] = self.CH4Model.calculate(dataDict)
        dataDict[ValuesNames.ch4LR.name] = self.CH4LRModel.calculate(dataDict)
        return dataDict

    def toDict(self):
        data = {
            "id" : self.id,
            "series1Ids" : self.series1Ids,
            "series2Ids" : self.series2Ids,
            "date" : self.date.strftime(timeformat),
            "models" : [
                {"V0Model" : self.V0Model.toDict()},
                {"CH4Model" : self.CH4Model.toDict()},
                {"CH4LRModel" : self.CH4LRModel.toDict()}
                ]
            }
        return data

    def toJsonString(self):
        return json.dumps(self.toDict(), indent=4)

    def fromJson(self, jsonDict):
        self.id = int(jsonDict['id'])
        self.series1Ids = jsonDict['series1Ids']
        self.series2Ids = jsonDict['series2Ids']
        self.date = dt.strptime(jsonDict['date'], timeformat)
        self.V0Model = self.calibrationModelFromJson(jsonDict['models'][0]['V0Model'])
        self.CH4Model = self.calibrationModelFromJson(jsonDict['models'][1]['CH4Model'])
        self.CH4LRModel = self.calibrationModelFromJson(jsonDict['models'][2]['CH4LRModel'])

    def calibrationModelFromJson(self, jsonDict):
        model = CalibrationModel()
        model.fromDict(jsonDict)
        return model



