# from enums import MeasureType, timeformat
# from series import Series

from operator import index
from datetime import datetime as dt
from typing import Optional

# from scipy.sparse import data
from .values import ValuesNames
from ..calibration.calibrationFunctions import RsR0_calc
import json

class ResultModel:
	
	def __init__(self) -> None:
		self.series1Id = series1Id
		self.series2Id = series2Id
		self.refDataId = refDataId

		self.V0Model = V0Model
		self.CH4Model = CH4Model
		self.CH4LRModel = CH4LRModel

	def calculateCH4(self, dataDict):
		dataDict[ValuesNames.voltage0.name] = self.V0Model.calculate(dataDict)
		dataDict[ValuesNames.rsr0.name] = RsR0_calc(dataDict)
		dataDict[ValuesNames.ch4.name] = self.CH4Model.calculate(dataDict)

class Model:

    str_index = "index"
    str_date = "date"
    str_calibrationId = "calibrationId"
    str_v_function = "functionVName"
    str_ch4_function = "functionCH4Name"
    str_v_predictors_count = "v_predictors_count"
    str_v_popt = "v_popt"
    str_v_pcov = "v_pcov"
    str_v_r_squared = "v_r_squared"
    str_v_adjusted_r_squared = "v_adjusted_r_squared"
    str_v_rmse = "v_rmse"
    str_ch4_predictors_count = "ch4_predictors_count"
    str_ch4_popt = "ch4_popt"
    str_ch4_pcov = "ch4_pcov"
    str_ch4_r_squared = "ch4_r_squared"
    str_ch4_adjusted_r_squared = "ch4_adjusted_r_squared"
    str_ch4_rmse = "ch4_rmse"
    str_k = "k"
    str_M = "M"

    def __init__(self, *args, **kwargs):
        jsonString = kwargs.get("jsonString", None)
        if jsonString:
            self.fromJson(jsonString)
        else:
            self.index                  = kwargs.get(Model.str_index, None) 
            self.date                   = kwargs.get(Model.str_date, None)
            self.calibrationId          = kwargs.get(Model.str_calibrationId, None)
            self.v_function             = kwargs.get(Model.str_v_function, None)
            self.ch4_function           = kwargs.get(Model.str_ch4_function, None)
            self.v_predictors_count     = kwargs.get(Model.str_v_predictors_count, None)
            self.v_popt                 = kwargs.get(Model.str_v_popt, None)
            self.v_pcov                 = kwargs.get(Model.str_v_pcov, None)
            self.v_r_squared            = kwargs.get(Model.str_v_r_squared, None)
            self.v_adjusted_r_squared   = kwargs.get(Model.str_v_adjusted_r_squared, None)
            self.v_rmse                 = kwargs.get(Model.str_v_rmse, None)
            self.ch4_predictors_count   = kwargs.get(Model.str_ch4_predictors_count  , None)
            self.ch4_popt               = kwargs.get(Model.str_ch4_popt, None)
            self.ch4_pcov               = kwargs.get(Model.str_ch4_pcov, None)
            self.ch4_r_squared          = kwargs.get(Model.str_ch4_r_squared, None)
            self.ch4_adjusted_r_squared = kwargs.get(Model.str_ch4_adjusted_r_squared, None)
            self.ch4_rmse               = kwargs.get(Model.str_ch4_rmse, None)
            self.k                      = kwargs.get(Model.str_k, None)
            self.M                      = kwargs.get(Model.str_M, None)

    def toJson(self):       
        data = {Model.str_index                 :self.index, 
                Model.str_date                  :self.date, 
                Model.calibrationId             :self.calibrationId, 
                Model.str_v_function            :self.v_function, 
                Model.str_ch4_function          :self.ch4_function,  
                Model.str_v_predictors_count    :self.v_predictors_count,
                Model.str_v_popt                :self.v_popt,
                Model.str_v_pcov                :self.v_pcov,
                Model.str_v_r_squared           :self.v_r_squared,
                Model.str_v_adjusted_r_squared  :self.v_adjusted_r_squared,
                Model.str_v_rmse                :self.v_rmse,
                Model.str_ch4_predictors_count  :self.ch4_predictors_count,
                Model.str_ch4_popt              :self.ch4_popt,
                Model.str_ch4_pcov              :self.ch4_pcov,
                Model.str_ch4_r_squared         :self.ch4_r_squared,
                Model.str_ch4_adjusted_r_squared:self.ch4_adjusted_r_squared,
                Model.str_ch4_rmse              :self.ch4_rmse,
                Model.str_k                     :self.k,
                Model.str_M                     :self.M
                }
        return json.dumps(data, indent=4)

    def fromJson(self, jsonString):
        self.index                  = int(jsonString[Model.str_index])
        self.date                   = dt.datetime.strptime(jsonString[Model.str_date], timeformat)
        self.calibrationId          = int(jsonString[Model.str_calibrationId])
        self.v_function             = jsonString[Model.str_v_function]
        self.ch4_function           = jsonString[Model.str_ch4_function]
        self.v_predictors_count     = int(jsonString[Model.str_v_predictors_count])
        self.v_popt                 = float(jsonString[Model.str_v_popt]) 
        self.v_pcov                 = float(jsonString[Model.str_v_pcov])
        self.v_r_squared            = float(jsonString[Model.str_v_r_squared])
        self.v_adjusted_r_squared   = float(jsonString[Model.str_v_adjusted_r_squared])
        self.v_rmse                 = float(jsonString[Model.str_v_rmse])
        self.ch4_predictors_count   = int(jsonString[Model.str_ch4_predictors_count])
        self.ch4_popt               = float(jsonString[Model.str_ch4_popt])
        self.ch4_pcov               = float(jsonString[Model.str_ch4_pcov])
        self.ch4_r_squared          = float(jsonString[Model.str_ch4_r_squared])
        self.ch4_adjusted_r_squared = float(jsonString[Model.str_ch4_adjusted_r_squared])
        self.ch4_rmse               = float(jsonString[Model.str_ch4_rmse])
        self.k                      = float(jsonString[Model.str_k])
        self.M                      = float(jsonString[Model.str_M])


