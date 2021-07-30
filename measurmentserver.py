from referenceData import ReferenceData
from measurement import Measurement
from measurementmodule import MeasurementModule
# from driver import Driver
import datetime as dt
from series import Series
from calibration import CalibrationModule
from measurementfilesystem import MeasurementFileSystem
from enums import MeasureType, Status

# EXEC_DIR = "/home/pi/Documents/Repos/poplavok-algorithm/MServer"
EXEC_DIR = "C:/Users/mershavka/Repositories/poplavok-algorithm/sandbox"

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
        if ms.currentCalibration:
            CH4 = ms.currentCalibration.calculateCH4(dataDict)
            dataDict[ch4String] = CH4
            
        ms.fs.writeMeasurementToFile(ms.currentMeasurement, dataDict)

    def __init__(self):
        if self.initialized:
            return
        # self.device = Driver()
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
        return new_series.toJson()

    def chooseSeries(self, id):
        if id in self.series.keys:
            self.currentSeries = self.series[id]
        else:	
            self.status = Status.ERROR
            print("No series with id={}".format(id))

    def addReferenceDataToSeries(self, path):
        if not self.currentSeries:
            print("Choose a Series before loading reference data")
            self.status = Status.ERROR
            return
        r = ReferenceData(seriesId=self.currentSeries.id, loadingDate=dt.datetime.now())
        self.currentSeries.referenceData = r
        self.fs.addReferenceDataToSeries(self.currentSeries, path)


    def runMeasurement(self, type, duration, periodicity, description):
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
            m_id += max(self.currentSeries.getMeasurementsIds)
        new_measurement = Measurement(seriesId=self.currentSeries.id, duration=duration, periodicity=periodicity, date=dt.datetime.now(), description=description, calibrationId=self.currentCalibration, id=m_id)
        self.fs.addMeasurement(new_measurement)
        self.currentSeries.addMeasurement(m_id, new_measurement)
        self.currentMeasurement = new_measurement
        self.worker.startMeasurement(new_measurement)
        self.status = MeasureType.toStatus(type)

    def interruptMeasurement(self):
        self.worker.stopMeasurement()
        self.status = Status.NO

    def chooseMeasurement(self, id):
        if self.currentSeries is None:
            print("Select a Series before choosing a measurement")
            return -1
        self.currentMeasurement = self.currentSeries.getMesurementById(id)
        if self.currentMeasurement is None:
            print("No measurement with id {} in the Series with id {}".format(id, self.currentSeries.id))
            return -1
        return 0

    def deleteCurrentMeasurement(self):
        if self.status in [Status.COMMON_MEASUREMENT, Status.CALIBRATION, Status.FIELD_EXPERIMENT]:
            print('Measurement is underway, stop it before deleting')
            return -1
        m = self.currentSeries.popMeasurement(self.currentMeasurement.id)
        self.fs.deleteMeasurement(m)
        return 0

    def getServerStatus(self):
        return self.status

    def getSeriesList(self):
        return [*self.series.values()]

    def getSeriesDict(self):
        return self.series
    
    def getStatus(self):
        if not self.worker.isWorking():
            self.status = Status.NO
        return self.status

    def chooseCalibration(self, id):
        if id in self.calibrations:
            self.currentCalibration = self.calibrations[id]
        else:	
            self.status = Status.ERROR
            print("No calibration with id={}".format(id))

    def startCalibration(self, seriesIdStep1, seriesIdStep2):
        pass

    def selectCH4Model(self, id):
        if not self.currentCalibration:
            print("Choose Calibration before selecting model")
    
    def gotIt(self):
        self.status = Status.NO
