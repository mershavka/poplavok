from enum import Enum

__all__ = ['timeformat', 'Status', 'MeasureType']

timeformat = "%Y%m%d%H%M%S"
class Status(Enum):
    NO 					= (0, "Nothing is happening")
    ERROR 				= (1, "Error occured")
    COMMON_MEASUREMENT 	= (2, "Uncallibrated experiment is underway")
    FIELD_EXPERIMENT 	= (3, "Callibrated experiment is underway")
    CALIBRATION 		= (4, "Experiment for calibration is underway")
    WARNING 			= (6, "Warning")

    def __init__(self, id, title):
        self.id = id
        self.title = title
    def info(self):
        print("Name - %s, id - %s, desription - %s"%(self.name, self.id, self.title))

class MeasureType(Enum):
    COMMON = 0
    EXPERIMENT = 1
    CALIBRATION_1 = 2
    CALIBRATION_2 = 3
    def toStatus(type):
        if type.value not in [item.value for item in MeasureType]:
            return None
        types = { MeasureType.COMMON : Status.COMMON_MEASUREMENT, MeasureType.EXPERIMENT : Status.FIELD_EXPERIMENT, 
            MeasureType.CALIBRATION_1 : Status.CALIBRATION, MeasureType.CALIBRATION_2 : Status.CALIBRATION}
        return types[type]

