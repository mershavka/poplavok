from enum import Enum
from datetime import datetime as dt

class Series:

	class SeriesType(Enum):
		COMMON = 0
		EXPERIMENT = 1
		CALIBRATION_1 = 2
		CALIBRATION_2 = 3

	def __init__(self, description="", type=SeriesType.COMMON):
			self.id = -1
			self.date = dt.now()
			self.description = description
			self.type = type

	def __str__(self) -> str:
		pass