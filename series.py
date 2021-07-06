import enum
import os
import datetime
import re

class Series:
	series_regex = "series(?P<id>\d+)_(?P<type>\d+)_(?P<date>\d+)"

	class SeriesType(enum.Enum):
		COMMON = 0
		EXPERIMENT = 1
		CALIBRATION_1 = 2
		CALIBRATION_2 = 3

	def __init__(self, path, id=None, description="", type=SeriesType.COMMON):
		if id != None:		

			self.id = id
			self.date = datetime.datetime.now()
			self.description = description
			self.type = type

			self.dir_name = "series{}_{}_{}".format(self.id, self.type.value, self.date.strftime("%Y%m%d%H%M%S"))
			self.dir_path = path + '/' + self.dir_name
			if not os.path.exists(self.dir_path):
				os.mkdir(self.dir_path)
			self.info_path = self.dir_path + '/info.txt'

			with open(self.info_path, 'w') as f:
				f.write("date={}\ndescription={}\ntype={}".format(self.date, self.description, self.type))
		else:
			pathStr = os.path.basename(os.path.normpath(path))
			matched = re.match(Series.series_regex, pathStr)
			if bool(matched):
				self.id = int(matched.group('id'))
				self.type = Series.SeriesType(int(matched.group('type')))
				date_time_obj = datetime.datetime.strptime(matched.group('date'),"%Y%m%d%H%M%S")
				self.date = date_time_obj

	def __str__(self) -> str:
		pass