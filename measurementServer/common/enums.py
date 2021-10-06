from enum import Enum

__all__ = ['timeformat', 'Status', 'MeasureType']

timeformat = "%Y%m%d%H%M%S"
class Status(Enum):
    NO 					= (0, "Ожидание")
    ERROR 				= (1, "Ошибка")
    COMMON_MEASUREMENT 	= (2, "Измерение без калибровки")
    FIELD_EXPERIMENT 	= (3, "Измерение с калибровкой")
    CALIBRATION 		= (4, "Калибровочные измерения")
    WARNING 			= (6, "Внимание")

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
    def getList():
        LIST = (
            (0, 'Измерения без калибровки'),
            (1, 'Измерния с калибровкой'),
            (2, 'Калибровочные измерения 1'),
            (3, 'Калибровочные измерения 2')
        )
        return LIST

    def toStatus(type):
        if type.value not in [item.value for item in MeasureType]:
            return None
        types = { MeasureType.COMMON : Status.COMMON_MEASUREMENT, MeasureType.EXPERIMENT : Status.FIELD_EXPERIMENT, 
            MeasureType.CALIBRATION_1 : Status.CALIBRATION, MeasureType.CALIBRATION_2 : Status.CALIBRATION}
        return types[type]

