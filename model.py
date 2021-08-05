from enums import MeasureType, timeformat
from datetime import datetime as dt
from series import Series
from typing import Optional
import json

class Model:
    def __init__(self, *args, **kwargs):
        pass

    def toJson(self):
        data = {'id': self.id}
        return json.dumps(data, indent=4)

    def fromJson(self, jsonString):
        self.id = int(jsonString["id"])
        self.date = dt.datetime.strptime(jsonString["date"], timeformat)
        self.v_function = jsonString["functionVName"]
        self.ch4_function = jsonString["functionCH4Name"]
        self.v_predictors_count = int(jsonString["v_predictors_count"])
        self.v_popt = float(jsonString["v_popt"]) 
        self.v_pcov = float(jsonString["v_pcov"])
        self.v_r_squared = float(jsonString["v_r_squared"])
        self.v_adjusted_r_squared = float(jsonString["v_adjusted_r_squared"])
        self.v_rmse = float(jsonString["v_rmse"])
        self.ch4_predictors_count = int(jsonString["ch4_predictors_count"])
        self.ch4_popt = float(jsonString["ch4_popt"])
        self.ch4_pcov = float(jsonString["ch4_pcov"])
        self.ch4_r_squared = float(jsonString["ch4_r_squared"])
        self.ch4_adjusted_r_squared = float(jsonString["ch4_adjusted_r_squared"])
        self.ch4_rmse = float(jsonString["ch4_rmse"])
        self.k = float(jsonString["k"])
        self.M = float(jsonString["M"])


