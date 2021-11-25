from pandas.core.frame import DataFrame
from measurementServer.common import referenceData
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
    refData_name_regex = "referenceData_series(?P<seriesId>\d+)_(?P<date>\d+)"
    result_model_name_regex = "resultModel(?P<id>\d+)_(?P<date>\d+)_(?P<functionV>\w+_\w+)_(?P<functionCH4>\w+_\w+)"

    def __init__(self, path):
        self.path = path
        self.refDir = 'ReferenceData'
        self.resultModelsDir = 'ResultModels'
        self.header = None
        if not os.path.exists(self.path):
            try:
                os.mkdir(self.path)
            except FileNotFoundError:
                self.path = os.getenv('HOME') + '/Poplavok'
                if not os.path.exists(self.path):
                    os.mkdir(self.path)
        
        self.refPath = self.path + '/' + self.refDir
        self.resultModelsPath = self.path + '/' + self.resultModelsDir

        if not os.path.exists(self.refPath):
            os.mkdir(self.refPath)

        if not os.path.exists(self.resultModelsPath):
            os.mkdir(self.resultModelsPath)
        

    def getReferenceDataDict(self, refData):
        if refData.valuesDict:
            return refData.valuesDict

        refDataPath = self.refDataToPath(refData)
        valuesDict = {}
        with open(refDataPath) as f:
            reader = csv.DictReader(f) # read rows into a dictionary format
            for row in reader: # read a row as {column1: value1, column2: value2,...}
                for (k,v) in row.items(): # go over each column name and value
                    if k == ValuesNames.timestamp.name:
                        v = datetime.datetime.strptime(v, timeformat)
                    else:
                        v = int(v)
                    valuesDict[k].append(v)
        refData.valuesDict = valuesDict
        return valuesDict

    def __pathToReferenceData(self, path):
        pathStr = os.path.basename(os.path.normpath(path))
        descriptionStr = os.path.splitext(pathStr)[0]
        matched = re.match(self.refData_name_regex, descriptionStr)
        if bool(matched):
            seriesId = int(matched.group('seriesId'))
            date = datetime.datetime.strptime(matched.group('date'), timeformat)
            return ReferenceData(seriesId, date)
        else:
            return None

    def __pathToResultModel(self, path):
        pathStr = os.path.basename(os.path.normpath(path))
        matched = re.match(self.result_model_name_regex, pathStr)
        if bool(matched):
            rm = ResultModel()
            with open(path) as json_file:
                jsonDict = json.load(json_file)
                rm.fromJson(jsonDict)
            return rm
        else:
            return None

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

            for filename in glob.glob(seriesPath + "/*.csv"):
                m = self.__pathToMeasure(filename)
                if m:
                    s.addMeasurement(m.id, m)
            return s
        else:
            return None    

    def getSeriesPathById(self, id):
        seriesPath = glob.glob(self.path + "/series{}*".format(id))
        if not seriesPath:
            return None
        return seriesPath[-1]

    def __seriesToPath(self, s: Series):
        return self.path + "/series{}_{}_{}".format(s.id, s.type.value, s.date.strftime(timeformat))

    def __measurementToPath(self, m: Measurement):
        seriesPath = self.getSeriesPathById(m.seriesId)
        return seriesPath + "/measure{}_{}_{}.csv".format(m.id, m.type.value, m.date.strftime(timeformat))

    def refDataToPath(self, refData: ReferenceData):
        refDataFileName = "/referenceData_series{}_{}.csv".format(refData.seriesId, refData.loadingDate.strftime(timeformat))
        refDataPath = self.refPath + refDataFileName
        return refDataPath

    def __resultModelToPath(self, bestModel : ResultModel):
        resultModelPath = self.resultModelsPath + "/resultModel{}_{}_{}_{}.json".format(bestModel.id, bestModel.date.strftime(timeformat), bestModel.V0Model.function_name, bestModel.CH4Model.function_name)
        return resultModelPath

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

    def loadReferencesData(self):
        refDataPathes = glob.glob(self.refPath + '/referenceData*.csv')
        refDataDict = {}
        for refDataPath in refDataPathes:
            refData = self.__pathToReferenceData(refDataPath)
            if refData is None:
                continue
            refDataDict[refData.seriesId] = refData
        return refDataDict

    def loadResultModels(self):
        modelsPathes = glob.glob(self.resultModelsPath + '/resultModel*.json')
        resultModelsDict = {}
        for modelPath in modelsPathes:
            resultModel = self.__pathToResultModel(modelPath)
            if resultModel is None:
                continue
            resultModelsDict[resultModel.id] = resultModel
        return resultModelsDict

    def addSeries(self, s: Series):
        seriesPath = self.__seriesToPath(s)
        if not os.path.exists(seriesPath):
            os.mkdir(seriesPath)
        jsonString = s.toJsonString()
        with open(seriesPath+'/description.json', 'w') as f:
            f.write(jsonString)
        return

    def addMeasurement(self, m : Measurement):
        measurementPath = self.__measurementToPath(m)
        jsonString = m.toJsonString()
        descriptionStr = os.path.splitext(measurementPath)
        descriptionStr = descriptionStr[0] + ".json"
        with open(descriptionStr, 'w') as f:
            f.write(jsonString)
        return

    def addReferenceData(self, refData: ReferenceData):
        referenceDataPath = self.refDataToPath(refData) 
        header = list(refData.valuesDict.keys())
        self.appendRowToCsv(referenceDataPath, header)        
        for item in zip(*list(refData.valuesDict.values())):
            self.appendRowToCsv(referenceDataPath, item)
        return

    def addResultModel(self, bestModel : ResultModel):
        bestModelPath = self.__resultModelToPath(bestModel)
        jsonString = bestModel.toJsonString()
        with open(bestModelPath, 'w') as f:
            f.write(jsonString)
        return

    def deleteMeasurement(self, m):
        measurementPath = self.__measurementToPath(m)
        os.remove(measurementPath)
        # удалить json?
        descriptionStr = os.path.splitext(measurementPath)[0] + ".json"
        os.remove(descriptionStr)

    def appendRowToCsv(self, filename, listOfElements):
        with open(filename, 'a+', newline='') as writeObj:
            writer = csv.writer(writeObj)
            writer.writerow(listOfElements)

    def writeMeasurementToFile(self, m, dataDict):
        m_path = self.__measurementToPath(m)
        if not os.path.exists(m_path):
            open(m_path, 'w').close()
            self.header = list(dataDict.keys()) 
            self.appendRowToCsv(m_path, self.header)
        
        dataList = [dataDict[valueName] for valueName in self.header]
        self.appendRowToCsv(m_path, dataList)
        return 0
