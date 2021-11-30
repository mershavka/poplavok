from ..common import timeformat
import json
import enum
from .msLogger import MsLogger

logger = MsLogger().get_logger()

class MeasurementServerRespone:
    
    STATUS_OK          = 0
    STATUS_WARNING     = 1
    STATUS_ERROR       = 2

    def __init__(self, status, data = None) -> None:
        self.status = status
        self.data_type = type(data).__name__
        try:
            if not data:
                self.data_string = ''
            elif type(data) is list:
                self.data_string = json.dumps([element.toJsonString() for element in data])
            elif type(data) is dict:
                self.data_string = json.dumps({key : value.toJsonString() for key, value in data.items()})
            else:
                self.data_string.toJsonString()
        except:
            logger.warning('Failed To Serialize Response Data')
            self.data_string = str(data)
            self.status = MeasurementServerRespone.STATUS_WARNING

    def OK():
        return MeasurementServerRespone(status=MeasurementServerRespone.STATUS_OK)
    
    def OK_DATA(data):
        return MeasurementServerRespone(status=MeasurementServerRespone.STATUS_OK, data=data)

    def toDict(self):
        data = {'status': self.status, 'data_string' : self.data_string, 'data_type': self.data_type}
        return data

    def toJsonString(self):
        return json.dumps(self.toDict(), indent=4)

    def fromJson(self, jsonDict):
        self.status         = int(jsonDict['status'])
        self.data_string    = jsonDict['data_string']
        self.data_type      = jsonDict['data_type']

    def __str__(self) -> str:
        return "STATUS: {}. DATA_TYPE: {}".format(self.status, self.data_type)