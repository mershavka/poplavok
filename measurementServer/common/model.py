from .enums import timeformat
# from series import Series

from operator import index
from datetime import datetime as dt
from typing import Optional

from measurementServer.calibration.calibrationModel import CalibrationModel

# from scipy.sparse import data
from .values import ValuesNames
from ..calibration.calibrationFunctions import RsR0_calc
import json

class ResultModel:
    
    def __init__(self, id:  Optional[int] = None, series1Id :  Optional[int] = None, series2Id:  Optional[int] = None, date=None, V0Model : Optional[CalibrationModel] = None, CH4Model : Optional[CalibrationModel] = None, CH4LRModel : Optional[CalibrationModel] = None) -> None:
        self.id = id
        self.series1Id = series1Id
        self.series2Id = series2Id

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

    def toJsonString(self):
        data = {
            "id" : self.id,
            "series1Id" : self.series1Id,
            "series2Id" : self.series2Id,
            "date" : self.date.strftime(timeformat),
            "models" : [
                {"V0Model" : self.V0Model.toDict()},
                {"CH4Model" : self.CH4Model.toDict()},
                {"CH4LRModel" : self.CH4LRModel.toDict()}
                ]
            }

        return json.dumps(data, indent=4)

    def fromJson(self, jsonDict):
        self.id = int(jsonDict['id'])
        self.series1Id = int(jsonDict['series1Id'])
        self.series2Id = int(jsonDict['series2Id'])
        self.date = dt.strptime(jsonDict['date'], timeformat)
        self.V0Model = self.calibrationModelFromJson(jsonDict['models'][0]['V0Model'])
        self.CH4Model = self.calibrationModelFromJson(jsonDict['models'][1]['CH4Model'])
        self.CH4LRModel = self.calibrationModelFromJson(jsonDict['models'][2]['CH4LRModel'])

    def calibrationModelFromJson(self, jsonDict):
        model = CalibrationModel()
        model.fromDict(jsonDict)
        return model



