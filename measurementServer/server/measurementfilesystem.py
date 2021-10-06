from ..common import *
from ..common.enums import *

import os
import re
import glob
import datetime
import json
import csv
from shutil import copy

class MeasurementFileSystem:
    series_name_regex = "series(?P<id>\d+)_(?P<type>\d+)_(?P<date>\d+)"
    measurement_name_regex = "measure(?P<id>\d+)_(?P<type>\d+)_(?P<date>\d+)"
    calibration_name_regex = "calibration(?P<id>\d+)_(?P<date>\d+)"
    model_name_regex = "model(?P<index>\d+)_(?P<functionV>\w+_\w+)_(?P<functionCH4>\w+_\w+)"

    def __init__(self, path):
        self.path = path
        self.header = None
        if not os.path.exists(self.path):
            try:
                os.mkdir(self.path)
            except FileNotFoundError:
                self.path = os.getenv('HOME') + '/Poplavok'
                if not os.path.exists(self.path):
                    os.mkdir(self.path)
    
    def __pathToMeasure(self, path):
        pathStr = os.path.basename(os.path.normpath(path))
        descriptionStr = os.path.splitext(path)[0] + ".json"
        matched = re.match(self.measurement_name_regex, pathStr)
        if bool(matched):
            m = Measurement()
            if not os.path.exists(descriptionStr):
                print("No description found for measurement")
                return None
            with open(descriptionStr) as json_file:
                jsonDict = json.load(json_file)
                m.fromJson(jsonDict)         
            return m
        else:
            return None

    def __pathToCalibration(self, path):
        calibrationDirName = os.path.basename(os.path.normpath(path))
        matched = re.match(self.calibration_name_regex, calibrationDirName)
        if bool(matched):
            c_id = int(matched.group('id'))
            c_date = datetime.datetime.strptime(matched.group('date'), timeformat)
            jsonPath = path + '/description.json'
            if not os.path.exists(jsonPath):
                return None
            with open(jsonPath) as json_file:
                data = json.load(json_file)
            if not data:
                return None
            c_desription = data['description']
            c_series1StepId = int(data['series1StepId'])
            c_series2StepId = int(data['series2StepId'])

            c_models = {}

            for filename in glob.glob(calibrationDirName + "/*.csv"):
                model = self.__pathToModel(filename)
                if model:
                    c_models[model.id] = model

            c = Calibration( id = c_id, series1StepId = c_series1StepId, series2StepId = c_series2StepId, date = c_date, description = c_desription, models=c_models)
            return c
        
        return None

    def __pathToSeries(self, seriesPath):
        seriesDirName = os.path.basename(os.path.normpath(seriesPath))
        matched = re.match(self.series_name_regex, seriesDirName)
        if bool(matched):
            s = Series()
            jsonPath = seriesPath + '/description.json'
            if not os.path.exists(jsonPath):
                return None
            with open(jsonPath) as json_file:
                data = s.fromJson(json.load(json_file))

            # if not data or int(data['id']) != s_id or int(data['type']) != s_type or datetime.datetime.strptime((data['date']), timeformat) != s_date:
            #     print("Invalid json description file for series")
            #     return None

            # s_desription = data['description']

            # s_measurements = {}
            # s_referenceData = {} #Как заполнять?

            for filename in glob.glob(seriesPath + "/*.csv"):
                m = self.__pathToMeasure(filename)
                if m:
                    s.addMeasurement(m.id, m)
            return s
        else:
            return None

    def __getSeriesPathById(self, id):
        seriesPath = glob.glob(self.path + "/series{}*".format(id))
        return seriesPath[-1]
        

    def __seriesToPath(self, s: Series):
        return self.path + "/series{}_{}_{}".format(s.id, s.type.value, s.date.strftime(timeformat))

    def __measurementToPath(self, m : Measurement):
        seriesPath = self.__getSeriesPathById(m.seriesId)
        return seriesPath + "/measure{}_{}_{}.csv".format(m.id, m.type.value, m.date.strftime(timeformat))

    def __modelToPath(self, model: Model):
        #TODO  SOLVE CALIBRATION PATH
        calibrationPath = ""
        return calibrationPath + "/model{}_{}_{}.csv".format(model.index, model.v_function, model.ch4function)

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
            if not os.path.isdir(calibrationPath):
                continue
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
        jsonString = s.toJsonString()
        with open(seriesPath+'/description.json', 'w') as f:
            f.write(jsonString)
        return

    def addMeasurement(self, m):
        measurementPath = self.__measurementToPath(m)
        if not os.path.exists(measurementPath):
            open(measurementPath, 'w').close()
        if self.header:	
            self.appendRowToCsv(measurementPath, self.header)
        jsonString = m.toJsonString()
        descriptionStr = os.path.splitext(measurementPath)
        descriptionStr = descriptionStr[0] + ".json"
        with open(descriptionStr, 'w') as f:
            f.write(jsonString)
        return

    def addCalibration(self, c):

        pass

    def addModel(self, model):
        modelPath = self.__modelToPath(model)
        pass

    def saveServerState(self, ms):
        pass

    def loadServerState(self, ms):
        pass
    
    def addReferenceDataToSeries(self, s, path):
        seriesPath = self.__seriesToPath(s)
        if not os.path.exists(seriesPath):
            return
        loadingDate = datetime.datetime.now()
        newReferenceDataPath = seriesPath + "/referenceData_loaded{}.csv".format(loadingDate.strftime(timeformat))
        resultPath = copy(path, newReferenceDataPath)
        s.referenceData = ReferenceData(seriesId = s.id, loadingDate=loadingDate)
        return s.referenceData

    def deleteMeasurement(self, m):
        measurementPath = self.__measurementToPath(m)
        os.remove(measurementPath)
        #удалить json?
        descriptionStr = os.path.splitext(measurementPath)[0] + ".json"
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
