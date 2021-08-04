from enums import MeasureType, timeformat
from datetime import datetime as dt
from series import Series
from typing import Optional
import json

class Model:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def toJson(self):
        data = {'id': self.id}
        return json.dumps(data, indent=4)

    def fromJson(self, jsonString):
        self.id = int(jsonString["id"])
        self.date = dt.datetime.strptime(jsonString["date"], timeformat)
