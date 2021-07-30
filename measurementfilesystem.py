from calibration import Calibration
from measurement import Measurement
import os
import re
import glob
import datetime
from series import Series
import json
import csv
from enums import MeasureType
from shutil import copy

class MeasurementFileSystem:
    series_name_regex = "series(?P<id>\d+)_(?P<type>\d+)_(?P<date>\d+)"
    measurement_name_regex = "measure(?P<id>\d+)_(?P<type>\d+)_(?P<date>\d+)"
    calibration_name_regex = "calibration(?P<id>\d+)_(?P<date>\d+)"
    timeformat = "%Y%m%d%H%M%S"

    def __init__(self, path):
        self.path = path
        self.header = None
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def __pathToSeries(self, path):
        seriesDirName = os.path.basename(os.path.normpath(path))
        matched = re.match(self.series_name_regex, seriesDirName)
        if bool(matched):
            s_id = int(matched.group('id'))
            s_type = MeasureType(int(matched.group('type')))
            s_date = datetime.datetime.strptime(matched.group('date'), MeasurementFileSystem.timeformat)
            jsonPath = path + '/description.json'
            if not os.path.exists(jsonPath):
                return None
            with open(jsonPath) as json_file:
                data = json.load(json_file)
                s_desription = data['description']

            s_measurements = None
            s_referenceData = None

            for filename in glob.glob(seriesDirName + "/*.csv"):
                # matched = re.match(self.series_name_regex, seriesDirName)
                #     if bool(matched):

                m = self.__pathToMeasure(filename)
                if m:
                    s_measurements[m.id] = m

            s = Series(id=s_id, description=s_desription, type=s_type, date=s_date, measurements=s_measurements, referenceData=s_referenceData)
            return s
        else:
            return None
    
    def __pathToMeasure(self, path):
        pathStr = os.path.basename(os.path.normpath(path))
        descriptionStr = os.path.splitext(pathStr[0] + ".json")
        matched = re.match(self.measurement_name_regex, pathStr)
        if bool(matched):
            m_id = int(matched.group('id'))
            m_type = MeasureType(int(matched.group('type')))
            m_date = datetime.datetime.strptime(
                matched.group('date'), MeasurementFileSystem.timeformat)
            with open(descriptionStr) as json_file:
                data = json.load(json_file)
            if not data:
                return None
            m_desription = data['description']
            m_seriesId = int(data['seriesId'])
            m_duration = float(data['duration'])
            m_periodicity = float(data['periodicity'])
            m_calibrationId = int(data['calibrationId'])
            m = Measurement(id=m_id, description=m_desription,
                       type=m_type, date=m_date, seriesId=m_seriesId, duration=m_duration,
                        periodicity=m_periodicity, calibrationId=m_calibrationId)
            return m
        else:
            return None

    def __pathToCalibration(self, path):
        pathStr = os.path.basename(os.path.normpath(path))
        descriptionStr = os.path.splitext(pathStr[0] + ".json")
        matched = re.match(self.calibration_name_regex, pathStr)
        if bool(matched):
            c_id = int(matched.group('id'))
            c_date = datetime.datetime.strptime(matched.group('date'), MeasurementFileSystem.timeformat)
            with open(descriptionStr) as json_file:
                data = json.load(json_file)
            if not data:
                return None
            c_desription = data['description']
            c_series1StepId = int(data['series1StepId'])
            c_series2StepId = int(data['series2StepId'])
            c = Calibration( id = c_id, series1StepId = c_series1StepId, series2StepId = c_series2StepId, date = c_date, description = c_desription)
            return c
        else:
            return None


    def __getSeriesPathById(self, id):
        seriesPath = glob.glob(self.path + "/series{}*".format(id))
        return seriesPath[-1]
        

    def __seriesToPath(self, s):
        return self.path + "/series{}_{}_{}".format(s.id, s.type.value, s.date.strftime(MeasurementFileSystem.timeformat))

    def __measurementToPath(self, m : Measurement):
        seriesPath = self.__getSeriesPathById(m.seriesId)
        return seriesPath + "/measure{}_{}_{}.csv".format(m.id, m.type.value, m.date.strftime(MeasurementFileSystem.timeformat))

    def loadSeries(self):
        seriesPathes = glob.glob(self.path + "/series*")
        seriesDict = {}
        for seriesPath in seriesPathes:
            if not os.path.isdir(seriesPath):
                continue
            s = self.__pathToSeries(seriesPath)
            if not s is None:
                seriesDict[s.id] = s
        return seriesDict

    def loadCalibrations(self):
        calibrationsPathes = glob.glob(self.path + "/calibrations/calibration*")
        calibrationsDict = {}
        for calibrationPath in calibrationsPathes:
            c = self.__pathToCalibration(calibrationPath)
            if not c is None:
                calibrationsDict[c.id] = c
        return calibrationsDict

    def setFileHeader(self, header):
        self.header = header

    def addSeries(self, s):
        seriesPath = self.__seriesToPath(s)
        if not os.path.exists(seriesPath):
            os.mkdir(seriesPath)
        jsonString = s.toJson()
        with open(seriesPath+'/description.json', 'w') as f:
            f.write(jsonString)
        return

    def addMeasurement(self, m):
        measurementPath = self.__measurementToPath(m)
        if not os.path.exists(measurementPath):
            open(measurementPath, 'w').close()
        if self.header:	
            self.appendRowToCsv(measurementPath, self.header)
        jsonString = m.toJson()
        descriptionStr = os.path.splitext(measurementPath)
        descriptionStr = descriptionStr[0] + ".json"
        with open(descriptionStr, 'w') as f:
            f.write(jsonString)
        return

    def addReferenceDataToSeries(self, s, path):
        seriesPath = self.__seriesToPath(s)
        if not os.path.exists(seriesPath):
            return
        newReferenceDataPath = seriesPath + "/referenceData_loaded{}.csv".format(r.loadingDate.strftime(MeasurementFileSystem.timeformat))
        resultPath = copy(path, newReferenceDataPath)

    def deleteMeasurement(self, m):
        measurementPath = self.__measurementToPath(m)
        os.remove(measurementPath)
        #удалить json?
        descriptionStr = os.path.splitext(measurementPath) + ".json"
        os.remove(descriptionStr)

    def appendRowToCsv(self, filename, listOfElements):
        with open(filename, 'a+', newline ='') as writeObj:
            writer = csv.writer(writeObj)
            writer.writerow(listOfElements)

    def writeMeasurementToFile(self, m, dataDict):
        m_path = self.__measurementToPath(m)
        if not self.header:
            print("No header for writing measurement data in file")
            return -1
        dataList = [dataDict[valueName] for valueName in self.header]
        self.appendRowToCsv(m_path, dataList)
        return 0
