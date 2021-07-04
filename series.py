import enum
import os

class Series:
	class SeriesType(enum.Enum):
		COMMON = (0, "Measurements without calibration")
		EXPERIMENT = (1, "Measurements with calibration")
		CALIBRATION_1 = (2, "Measurements for calibration (first step)")
		CALIBRATION_2 = (3, "Measurements for calibration (second step)")

		def __init__(self, id, title):
			self.id = id
			self.title = title
		def info(self):
			print("Name - %s, id - %s, desription - %s"%(self.name, self.id, self.title))

	def __init__(self, dir, id=None, name="", description="", type=SeriesType.COMMON):
		if (id == None):
			if ~os.path.isdir(dir):
		else:
		pass

	def __str__(self) -> str:
		pass