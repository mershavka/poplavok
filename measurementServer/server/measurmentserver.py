from logging import Logger
from ..common import *
from .measurementmodule import MeasurementModule
from .measurementfilesystem import MeasurementFileSystem
from .methaneAnalyzer import MethaneAnalyzer
from .msLogger import MsLogger
from ..calibration import CalibrationResult

import datetime as dt

# EXEC_DIR = "/home/pi/Documents/Repos/poplavok-algorithm/MServer"
EXEC_DIR = "C:/Users/mershavka/Repositories/poplavok-algorithm/sandbox"

class MeasurementServer:

    testMode = True
    initialized = False

    def now(self):
        return dt.datetime.now()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MeasurementServer, cls).__new__(cls)
        return cls.instance

    def __readFromDevice(sender):
        ms = MeasurementServer()
        if MeasurementServer.testMode:
            return { 	
                        ValuesNames.timestamp.name	: dt.datetime.now(),  
                        ValuesNames.adc.name			: 2044,
                        ValuesNames.voltage.name		: 1.2,
                        ValuesNames.temperature.name	: 25,
                        ValuesNames.rHumidity.name	    : 35, 
                        ValuesNames.aHumidity.name      : 10,
                        ValuesNames.pressure.name	    : 10000,
                    }
        
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

    def __init__(self):
        if self.initialized:
            return

        if not MeasurementServer.testMode:            
            from ..drivers import Driver
            self.device = Driver()
            self.device.open()

        self.logger = MsLogger().get_logger()
        self.logger.info("Hello, Logger! From MeasurementServer")

        self.fs = MeasurementFileSystem(EXEC_DIR)
        self.ma = MethaneAnalyzer()        

        self.series = self.fs.loadSeries()
        self.refDatas = self.fs.loadReferencesData()
        self.resultModels = self.fs.loadResultModels()
        self._config = self.fs.loadConfig()

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

    def createSeries(self, description="", type=MeasureType.COMMON):		
        new_series = Series(description=description, type=type, id = self.lastSeriesId + 1, date=dt.datetime.now())
        if new_series:
            self.lastSeriesId += 1
            self.fs.addSeries(new_series)
            self.series[new_series.id] = new_series
            self.currentSeries = new_series
        return new_series

    def chooseSeries(self, seriesId):
        if seriesId in self.series.keys():
            self.currentSeries = self.series[seriesId]
        else:	
            self.status = Status.ERROR
            self.logger.error("No series with id={}".format(seriesId))
        return self.currentSeries

    def uploadReferenceData(self, seriesId, timestampsList, ch4RefList):
        valuesDict = {ValuesNames.timestamp.name : timestampsList, ValuesNames.ch4Ref.name : ch4RefList}        
        refData = ReferenceData(seriesId, self.now(), valuesDict)
        self.fs.addReferenceData(refData)
        self.refDatas[refData.seriesId] = refData
        return

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
                return
            calibrationId = -1
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
        else:
            dataDict = self.device.readData()
            return self.addCH4toDict(dataDict)

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

    def startCalibration(self, seriesIdStep1, seriesIdStep2):        
        series1Path = self.fs.getSeriesPathById(seriesIdStep1) # Путь к серии для калибровки V0
        series2Path = self.fs.getSeriesPathById(seriesIdStep2) # Путь к серии для калибровки CH4

        if not (series1Path and series2Path):
            self.logger.error("Series not found!")
            return None

        if not (seriesIdStep2 in self.refDatas.keys()):
            self.logger.error("Reference data not found!")
            return None

        refDataPath = self.fs.refDataToPath(self.refDatas[seriesIdStep2])
        methaneModels_df, methaneModels_dict, bestMethaneModelDict = self.ma.calibration(series1Path, series2Path, refDataPath)
        if bestMethaneModelDict:
            id = self.lastResultModelId + 1
            self.lastResultModelId = id
            bestMethaneModel = CalibrationResult(id=id, date=dt.datetime.now(), series1Id=seriesIdStep1, series2Id=seriesIdStep2, V0Model=bestMethaneModelDict[ModelNames.model1], CH4Model=bestMethaneModelDict[ModelNames.model2], CH4LRModel=bestMethaneModelDict[ModelNames.model3])
            self.fs.addResultModel(bestMethaneModel)
            self.resultModels[id] = bestMethaneModel
            self.currentCalibration = bestMethaneModel
            return bestMethaneModel
        self.logger.error("Calibration failed, no model found")



