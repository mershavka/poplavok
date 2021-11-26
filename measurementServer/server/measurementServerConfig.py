import json
from dataclasses import dataclass

@dataclass
class MeasurementServerConfig:

    currentCalibrationId : int = -1

    def toDict(self):
        return {'currentCalibrationId' : self.currentCalibrationId}

    def toJsonString(self):
        return json.dumps(self.toDict(), indent=4)

    def fromJson(self, jsonDict):
        self.currentCalibrationId = int(jsonDict['currentCalibrationId'])