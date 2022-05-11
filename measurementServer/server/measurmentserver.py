from operator import index
from ..common import *
from .measurementmodule import MeasurementModule
from .measurementfilesystem import MeasurementFileSystem
from .methaneAnalyzer import MethaneAnalyzer
from .msLogger import MsLogger
from ..calibration import CalibrationResult

import datetime as dt

class MeasurementServer:

    initialized = False

    def now(self):
        return dt.datetime.now()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MeasurementServer, cls).__new__(cls)
        return cls.instance

    def __readFromDevice(sender):
        ms = MeasurementServer()        
        return ms.device.readData()
 
    def __writeToMeasureFile(sender, dataDict: dict):
        ms = MeasurementServer()
        if not ms.currentCalibration is None:
            dataDict = ms.currentCalibration.calculateCH4(dataDict)
        ms.lastData = dataDict   
        ms.fs.writeMeasurementToFile(ms.currentMeasurement, dataDict)

    def _measurementStopStatus(sender):
        ms = MeasurementServer()
        ms.status = Status.NO

    def __init__(self, path : str ='MS_DATA', testMode : bool = True):
        if self.initialized:
            return
            
        self.path = path
        self.fs = MeasurementFileSystem(self.path)
        self.logger = MsLogger().get_logger()

        self.testMode = testMode
        if not self.testMode:
            try:            
                from ..drivers.driver import Driver
                self.device = Driver()
                self.device.open()
            except Exception as e:
                self.logger.error(e)
        else:
            from ..drivers.testDriver import TestDriver
            self.device = TestDriver()
            self.device.open()

        

        self.logger.info("Path = {}, testModeOn = {}".format(path, testMode))

        self.ma = MethaneAnalyzer(self.path)        

        self.series         = self.fs.loadSeries()
        self.refDatas       = self.fs.loadReferencesData()
        self.resultModels   = self.fs.loadResultModels()
        self._config        = self.fs.loadConfig()

        self.lastSeriesId = 0 if not self.series else max(self.series.keys())
        self.lastResultModelId = 0 if not self.resultModels else max(self.resultModels.keys())

        self.worker = MeasurementModule()
        self.worker.setReadFunc(self.__readFromDevice)
        self.worker.setWriteFunc(self.__writeToMeasureFile)
        self.worker.setStopFunc(self._measurementStopStatus)

        # Status variables
        self.lastData = {}
        self.status = Status.NO
        self.currentSeries = None
        self.currentMeasurement = None

        if self._config.currentCalibrationId in self.resultModels.keys():
            self._currentCalibration = self.resultModels[self._config.currentCalibrationId]
        else:
            self.currentCalibration = None

        self.initialized = True
        self.logger.debug('MeasurementServer initialized')
    
    @property
    def currentCalibration(self):
        return self._currentCalibration

    @currentCalibration.setter
    def currentCalibration(self, value):
        self._currentCalibration = value
        if self.currentCalibration:
            self._config.currentCalibrationId = self._currentCalibration.id
        else:
            self._config.currentCalibrationId = -1
        self.fs.updateConfig(self._config)

    def getLogger(self):
        return self.logger

    def createSeries(self, description="", type=MeasureType.COMMON):		
        new_series = Series(description=description, type=type, id = self.lastSeriesId + 1, date=dt.datetime.now())
        if new_series:
            self.lastSeriesId += 1
            self.fs.addSeries(new_series)
            self.series[new_series.id] = new_series
            self.currentSeries = new_series
            self.logger.info("Series {} created".format(new_series.id))
        return new_series

    def chooseSeries(self, seriesId):
        if seriesId in self.series.keys():
            self.currentSeries = self.series[seriesId]
        else:	
            self.status = Status.ERROR
            self.logger.error("No series with id={}".format(seriesId))
        self.logger.info("Current series: {} ".format(self.currentSeries.id))
        return self.currentSeries

    def uploadReferenceData(self, seriesId, timestampsList, ch4RefList):
        valuesDict = {ValuesNames.timestamp.name : timestampsList, ValuesNames.ch4Ref.name : ch4RefList}        
        refData = ReferenceData(seriesId, self.now(), valuesDict)
        if refData:
            self.fs.addReferenceData(refData)
            self.refDatas[refData.seriesId] = refData
            self.logger.info("Reference data for series №{} successfully added".format(seriesId))
            return True
        self.logger.error("Failed to add reference data for series №{}".format(seriesId))
        return False

    def runMeasurement(self, duration, periodicity, description):
        if not self.currentSeries:
            self.status = Status.ERROR
            self.logger.error('Choose a series before measuring')
            return
        type = self.currentSeries.type
        if type != self.currentSeries.type:
            self.status = Status.ERROR
            self.logger.warning("Measurement and Series types are different")
            return
        if not self.currentCalibration:
            if type == MeasureType.EXPERIMENT:
                self.logger.error("No calibration")
            calibrationId = -1
        else:
            calibrationId = self.currentCalibration.id
        m_id = 1
        if self.currentSeries.getMeasurementsIds():
            m_id += max(self.currentSeries.getMeasurementsIds())		
        new_measurement = Measurement(seriesId=self.currentSeries.id, duration=duration, periodicity=periodicity, date=dt.datetime.now(), description=description, calibrationId=calibrationId, id=m_id)
        self.fs.addMeasurement(new_measurement)
        self.currentSeries.addMeasurement(m_id, new_measurement)
        self.currentMeasurement = new_measurement
        self.worker.startMeasurement(new_measurement)
        self.status = MeasureType.toStatus(type)
        return new_measurement

    def interruptMeasurement(self):
        self.worker.stopMeasurement()
        self.status = Status.NO
        return "Interrupted"

    def chooseMeasurement(self, id):
        if self.currentSeries is None:
            self.logger.error("Select a Series before choosing a measurement")
            return None
        self.currentMeasurement = self.currentSeries.getMesurementById(id)
        if self.currentMeasurement is None:
            self.logger.error("No measurement with id {} in the Series with id {}".format(id, self.currentSeries.id))
            return None
        return self.currentMeasurement

    def deleteCurrentMeasurement(self):
        if self.status in [Status.COMMON_MEASUREMENT, Status.CALIBRATION, Status.FIELD_EXPERIMENT]:
            self.logger.warning('Measurement is underway, stop it before deleting')
            return -1
        if self.currentMeasurement:
            m = self.currentSeries.popMeasurement(self.currentMeasurement.id)
            self.fs.deleteMeasurement(m)
            return 0
        self.logger.error("Current measurement not found")
        return -1

    def getCurrentSeries(self):
        return self.currentSeries

    def getCurrentMeasurement(self):
        return self.currentMeasurement

    def getServerStatus(self):
        return self.status

    def getSeriesList(self):
        return [*self.series.values()]
    
    def getSeriesDict(self):
        return self.series

    def getSeriesById(self, id):
        if id in self.series.keys():
            return self.series[id]
        return None

    def getSeriesPath(self, id):
        if id in self.series:
            return self.fs.getSeriesPathById(id)
        self.logger.warning("No series with id = {}".format(id))

    def getMeasurementPath(self, series_id, measurement_id):
        if series_id in self.series:
            return self.fs.getMeasurementPathById(series_id=series_id, measurement_id=measurement_id)
        self.logger.warning("No series with id = {}".format(series_id))
        return None
    
    def getReferenceDataPath(self, seriesId):
        if seriesId in self.refDatas:
            return self.fs.refDataToPath(self.refDatas[seriesId])
        return 

    def getMeasurementsList(self, seriesId):
        s = self.series[seriesId]
        m = s.getMeasurementsDict()
        return [*m.values()]
    
    def getStatus(self):
        if not self.worker.isWorking():
            self.status = Status.NO
        return self.status

    def getLastData(self):
        if self.worker.isWorking():
            return self.lastData

        dataDict = self.device.readData()
        if self.currentCalibration:
            dataDict = self.currentCalibration.calculateCH4(dataDict)
        return dataDict

    def getCurrentCalibration(self):
        return self.currentCalibration

    def chooseCalibration(self, id):
        if id in self.resultModels:
            self.currentCalibration = self.resultModels[id]
            return self.currentCalibration
        else:	
            self.status = Status.ERROR
            self.logger.error("No calibration with id={}".format(id))
            return None

    def getCalibrationsList(self):
        return [*self.resultModels.values()]

    

    def firstStepOfCalibration(self, seriesIdsStep1):
        self.logger.info('Into StartCalibration')      
        series1Paths = [] # Пути к сериям для калибровки V0
        for id in seriesIdsStep1:
            path = self.fs.getSeriesPathById(id) 
            if not path:
                self.logger.error("Series with id not found!".format(id))
                continue
            series1Paths.append(path)
        
        result = self.ma.firstStepCalibration(series1Paths, seriesIdsStep1)
        print(result)
        return result

    def startCalibration(self, seriesIdsStep1, seriesIdsStep2): 
        self.logger.info('Into StartCalibration')
        series1Paths = []
        series2Paths = []
        refDataPaths = []
        for id in seriesIdsStep1:
            path = self.fs.getSeriesPathById(id)
            if not path:
                self.logger.error("Series for step 1 with id = {} not found!".format(id))
                return None
            series1Paths.append(path) # Путь к серии для калибровки V0

        for id in seriesIdsStep2:
            path = self.fs.getSeriesPathById(id)
            if not path:
                self.logger.error("Series for step 2 with id = {} not found!".format(id))
                return None
            if not (id in self.refDatas.keys()):
                self.logger.error("Reference data for series with id = {} not found!".format(id))
                return None
            series2Paths.append(path) # Путь к серии для калибровки CH4
            refDataPaths.append(self.fs.refDataToPath(self.refDatas[id]))

        if not (series1Paths and series2Paths):
            self.logger.error("Series not found!")
            return None

        series2data_df, methaneModels_dict, bestMethaneModelDict = self.ma.calibration(series1Paths, series2Paths, refDataPaths, seriesIdsStep1, seriesIdsStep2)
        if bestMethaneModelDict:
            id = self.lastResultModelId + 1
            self.lastResultModelId = id
            bestMethaneModel = CalibrationResult(id=id, date=dt.datetime.now(), series1Ids=seriesIdsStep1, series2Ids=seriesIdsStep2, V0Model=bestMethaneModelDict[ModelNames.model1], CH4Model=bestMethaneModelDict[ModelNames.model2], CH4LRModel=bestMethaneModelDict[ModelNames.model3])
            self.fs.addResultModel(bestMethaneModel)
            self.resultModels[id] = bestMethaneModel
            self.currentCalibration = bestMethaneModel
            self.logger.info("Sucessfull calibration")
            try:
                df_calculated = bestMethaneModel.calculateCH4(series2data_df)
                df_calculated.sort_values(by=[ValuesNames.timestamp.name], inplace=True)
                formats = {ValuesNames.temperature.name : '{:.1f}', ValuesNames.rHumidity.name : '{:.1f}', ValuesNames.aHumidity.name : '{:.5f}', ValuesNames.pressure.name : '{:.1f}', ValuesNames.ch4LR.name : '{:.3f}', ValuesNames.ch4.name : '{:.3f}', ValuesNames.ch4Ref.name : '{:.3f}'}

                for col, f in formats.items():
                    df_calculated[col] = df_calculated[col].map(lambda x: f.format(x))
                df_calculated.to_csv('test_recalculation_{}.csv'.format("_".join(map(str, seriesIdsStep1+seriesIdsStep2))), index=None, float_format='%.5f')
            except Exception as e:
                self.logger.error("Не удалось рассчитать значения по лучшей модели")
            return bestMethaneModel
        self.logger.error("Calibration failed, no model found")
        return None

    def startRecalibration(self, seriesId, calibrationId):
        seriesPath = self.fs.getSeriesPathById(seriesId) #Путь к серии с данными
        if not seriesPath:
            self.logger.error("Series not found!")
            return None
        if not (seriesId in self.refDatas.keys()):
            self.logger.error("Reference data for series with id = {} not found!".format(seriesId))
            return None
        if not calibrationId in self.resultModels.keys():
            self.logger.error("Calibration with id = {} not found!".format(calibrationId))
            return None
        refDataPath = self.fs.refDataToPath(self.refDatas[seriesId])
        oldCalibrationResult = self.resultModels[calibrationId]
        resultModel3 = self.ma.recalibration(seriesPath, refDataPath)
        recalibrationResult = CalibrationResult(date=dt.datetime.now(), series1Ids=oldCalibrationResult.series1Ids, series2Ids=oldCalibrationResult.series2Ids, V0Model=oldCalibrationResult.V0Model, CH4Model=oldCalibrationResult.CH4Model, CH4LRModel=resultModel3)
        recalibrationResultWithId = self.updateCurrentCalibration(recalibrationResult)
        return recalibrationResultWithId

    def updateCurrentCalibration(self, calibrationResult : CalibrationResult):
            id = self.lastResultModelId + 1
            self.lastResultModelId = id
            calibrationResult.id = id
            self.fs.addResultModel(calibrationResult)
            self.resultModels[id] = calibrationResult
            self.currentCalibration = calibrationResult
            return calibrationResult

    def getRefDatas(self):
        return self.refDatas
    
    def getRefIdsList(self):
        return list(self.refDatas.keys())

    def setFansSpeed(self, percentage = 100):
        self.device.pca_set_fans_speed(percentage)
        self.logger.info('Fans speed value: ' + str(percentage))

    def plotMeasurement(self, variable, series_id, measurement_id):
        measurement_path = self.getMeasurementPath(series_id, measurement_id)
        if not measurement_path:
            self.logger.error('No measurement with id = {} in series with id = {}'.format(measurement_id, series_id))
            return None
        image_path = self.ma.plotMeasurement(variable=variable, path=measurement_path)
        if not image_path:
            self.logger.error("Failed to graph {} from measurement with id = {} in series with id {}".format(variable, measurement_id, series_id))
        return image_path
        