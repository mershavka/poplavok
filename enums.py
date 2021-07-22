from enum import Enum

class MeasureType(Enum):
    COMMON = 0
    EXPERIMENT = 1
    CALIBRATION_1 = 2
    CALIBRATION_2 = 3

class Status(Enum):
    NO 					= (0, "Nothing is happening")
    ERROR 				= (1, "Error occured")
    COMMON_EXPERIMENT 	= (2, "Uncallibrated experiment is underway")
    FIELD_EXPERIMENT 	= (3, "Callibrated experiment is underway")
    CALIBRATION_1 		= (4, "Experiment for calibration (first step) is underway")
    CALIBRATION_2 		= (5, "Experiment for calibration (second step) is underway")
    WARNING 			= (6, "Warning")

    def __init__(self, id, title):
        self.id = id
        self.title = title
    def info(self):
        print("Name - %s, id - %s, desription - %s"%(self.name, self.id, self.title))