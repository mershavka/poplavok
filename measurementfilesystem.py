import os, re, glob, datetime
from series import Series

class MeasurementFileSystem:
    lastSeriesId = 0
    series_name_regex = "series(?P<id>\d+)_(?P<type>\d+)_(?P<date>\d+)"
    timeformat = "%Y%m%d%H%M%S"

    def __pathToSeries(self, path):
        pathStr = os.path.basename(os.path.normpath(path))
        matched = re.match(self.series_name_regex, pathStr)
        if bool(matched):
            id = int(matched.group('id'))
            type = Series.SeriesType(int(matched.group('type')))
            date = datetime.datetime.strptime(
                matched.group('date'), MeasurementFileSystem.timeformat)
            with open(pathStr + '/description.txt') as f:
                desription = f.read()
        else:
            return None

    def __seriesToPath(self, s):
        return self.path + "/series{}_{}_{}".format(s.id, s.type.value, s.date.strftime(MeasurementFileSystem.timeformat))

    def __loadSeries(self):
        seriesPathes = glob.glob(self.path + "/series*")
        for seriesPath in seriesPathes:
            s = self.__pathToSeries(seriesPath)
            if s is None:
                continue
            self.series[s.id] = s            
            if (s.id > self.lastSeriesId):
                self.lastSeriesId = s.id

    def __init__(self, path) -> None:
        self.path = path
        self.series = {}        
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        else:
            self.__loadSeries()

    def addSeries(self, s):
        s.id = self.lastSeriesId
        self.lastSeriesId += 1
        seriesPath = self.__seriesToPath(s)
        if not os.path.exists(seriesPath):
            os.mkdir(seriesPath)
        with open(seriesPath+'/description.txt', 'w') as f:
            f.write(self.description)
        return s.id

    def addMeasurement(self, series_id):
        pass

    def getSeriesList(self):
        return self.series.values

    def getMeasurementsList(self, series_id):
        pass