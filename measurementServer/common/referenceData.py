from .enums import timeformat

from datetime import datetime as dt
from typing import Optional
import json

class ReferenceData:

    def __init__(self, seriesId, loadingDate):
        self.seriesId = seriesId
        self.loadingDate = loadingDate

    def fromJson(self, jsonDict):
        self.seriesId = int(jsonDict['seriesId'])
        self.loadingDate = dt.strptime(jsonDict['loadingDate'], timeformat)

    def toDict(self):
        data = {'seriesId': self.seriesId, 'loadingDate': self.loadingDate.strftime(timeformat)}        
        return data
        
    def toJsonString(self):
        return json.dumps(self.toDict(), indent=4)