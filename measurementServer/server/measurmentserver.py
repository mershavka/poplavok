from ..common import *
from ..drivers import *
# from calibration import CalibrationModule
from .measurementfilesystem import MeasurementFileSystem
from .measurementmodule import MeasurementModule
import datetime as dt

EXEC_DIR = "/home/pi/Documents/Repos/poplavok-algorithm/MServer"
# EXEC_DIR = "C:/Users/mershavka/Repositories/poplavok-algorithm/sandbox"

class Error(Exception):
    """Base class for other exceptions"""
    pass

class BoardConnectionError(Error):
    pass

class FilePathError(Error):
    pass

timeString = 'Time'
adcString = 'ADC value'
voltageString = 'Voltage, V'
resistanceString = 'Resistance, Om'
temperatureString = 'Temperature, C'
rHumidityString = 'Related Humidity, %'
aHumidityString = 'Absolute Humidity, kg/m^3'
pressureString = 'Pressure, hPa'
ch4String = 'CH4, ppm'

class MeasurementServer:

    testMode = False
    initialized = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MeasurementServer, cls).__new__(cls)
        return cls.instance

    def __readFromDevice(sender):
        ms = MeasurementServer()
        if MeasurementServer.testMode:
            return { timeString: dt.datetime.now(),  adcString: 2044,
                         voltageString: 1.2,  resistanceString: 3000, 
                         temperatureString: 25,  rHumidityString: 35, 
                         aHumidityString: 10,  pressureString: 10000,  ch4String: 0}
        
        return ms.device.readData()
 
    def __writeToMeasureFile(sender, dataDict: dict):
        ms = MeasurementServer()
        # Расчет метана по калибровке
        newDataDict = ms.addCH4toDict(dataDict)
        ms.lastData = newDataDict   
        ms.fs.writeMeasurementToFile(ms.currentMeasurement, newDataDict)

    def _measurementStopStatus(sender):
        ms = MeasurementServer()
        ms.status = Status.NO

    def __init__(self):
        if self.initialized:
            return
        if not MeasurementServer.testMode:
            self.device = Driver()
            self.device.open()
        self.fs = MeasurementFileSystem(EXEC_DIR)        
        self.series = self.fs.loadSeries()
        self.calibrations = self.fs.loadCalibrations()
        if self.series:
            self.lastSeriesId = max(self.series.keys())
        else:
            self.lastSeriesId = 0
        self.lastCalibrationId = 0 if not self.calibrations else max(self.calibrations.keys())
        self.worker = MeasurementModule()
        self.worker.setReadFunc(self.__readFromDevice)
        self.worker.setWriteFunc(self.__writeToMeasureFile)
        self.worker.setStopFunc(self._measurementStopStatus)
        self.lastData = {}

        # Status variables
        self.status = Status.NO
        self.currentSeries = None
        self.currentMeasurement = None
        self.currentCalibration = None

        self.header = [	 timeString,  adcString,
                         voltageString,  resistanceString, 
                         temperatureString,  rHumidityString, 
                         aHumidityString,  pressureString,  ch4String]
        self.fs.setFileHeader(self.header)
        self.initialized = True

    def createSeries(self, description="", type=MeasureType.COMMON):		
        new_series = Series(description=description, type=type, id = self.lastSeriesId + 1, date=dt.datetime.now())
        if new_series:
            self.lastSeriesId += 1
            self.fs.addSeries(new_series)
            self.series[new_series.id] = new_series
            self.currentSeries = new_series
        return new_series.toJsonString()

    def chooseSeries(self, seriesId):
        if seriesId in self.series.keys():
            self.currentSeries = self.series[seriesId]
        else:	
            self.status = Status.ERROR
            print("No series with id={}".format(seriesId))
        return self.currentSeries

    def addReferenceDataToSeries(self, path):
        if not self.currentSeries:
            print("Choose a Series before loading reference data")
            self.status = Status.ERROR
            return
        self.fs.addReferenceDataToSeries(self.currentSeries, path)
        return self.currentSeries.referenceData


    def runMeasurement(self, duration, periodicity, description):
        type = self.currentSeries.type
        if not self.currentSeries:
            self.status = Status.ERROR
            print('Choose a series before measuring')
            return
        if type != self.currentSeries.type:
            self.status = Status.ERROR
            print("Measurement and Series types are different")
            return
        m_id = 1
        if self.currentSeries.getMeasurementsIds():
            m_id += max(self.currentSeries.getMeasurementsIds())
        new_measurement = Measurement(seriesId=self.currentSeries.id, duration=duration, periodicity=periodicity, date=dt.datetime.now(), description=description, calibrationId=self.currentCalibration, id=m_id)
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
            print("Select a Series before choosing a measurement")
            return None
        self.currentMeasurement = self.currentSeries.getMesurementById(id)
        if self.currentMeasurement is None:
            print("No measurement with id {} in the Series with id {}".format(id, self.currentSeries.id))
            return None
        return self.currentMeasurement

    def deleteCurrentMeasurement(self):
        if self.status in [Status.COMMON_MEASUREMENT, Status.CALIBRATION, Status.FIELD_EXPERIMENT]:
            print('Measurement is underway, stop it before deleting')
            return -1
        if self.currentMeasurement:
            m = self.currentSeries.popMeasurement(self.currentMeasurement.id)
            self.fs.deleteMeasurement(m)
            return 0
        print("Current measurement not found")
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
        if id in self.calibrations:
            self.currentCalibration = self.calibrations[id]
            return self.currentCalibration
        else:	
            self.status = Status.ERROR
            print("No calibration with id={}".format(id))
            return None

    def startCalibration(self, description, seriesIdStep1, seriesIdStep2):        
        series1Path = self.fs.getSeriesPathById(seriesIdStep1) # Путь к серии для калибровки V0
        series2Path = self.fs.getSeriesPathById(seriesIdStep2) # Путь к серии для калибровки CH4
        if not (series1Path and series2Path):
            print("Series not found!")
            return None
        c = Calibration(self.lastCalibrationId, seriesIdStep1, seriesIdStep2, dt.datetime.now(), description)
        self.currentCalibration = c


    def getCurrentCalibrationModels(self):
        if self.currentCalibration:
            return self.currentCalibration.models
        print("Choose Calibration before getting models")
        return None

    def selectCH4Model(self, id):
        if not self.currentCalibration:
            print("Choose Calibration before selecting model")
            return None
        if id in self.currentCalibration.models:
            self.currentCalibration.selectedModel = self.currentCalibration.models[id]
            return self.currentCalibration.selectedModel
        self.status = Status.ERROR
        print("No model with id={} in current calibration with id={}".format(id, self.currentCalibration.id))
        return None

    def gotIt(self):
        self.status = Status.NO

    def calculateCH4(self):
        pass

    def addCH4toDict(self, dataDict):
        if self.currentCalibration:
            CH4 = self.currentCalibration.calculateCH4(dataDict)
            dataDict[ch4String] = CH4
        else:
            dataDict[ch4String] = -1
        return dataDict
