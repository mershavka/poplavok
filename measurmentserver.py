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

    def __writeToMeasureFile(sender, data):
        ms = MeasurementServer()
        # Расчет метана по калибровке
        if ms.currentCalibration:
            ms.calculateCH4()
        ms.fs.writeMeasurementToFile(ms.currentMeasurement, data)

    def __init__(self):
        if self.initialized:
            return
        self.series = {}
        # self.device = Driver()
        self.fs = MeasurementFileSystem(EXEC_DIR)        
        self.series = self.fs.loadSeries()
        if self.series:
            self.lastSeriesId = max(self.series.keys())
        else:
            self.lastSeriesId = 0
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

    def runMeasurement(self, type, duration, periodicity, description):
        if not self.currentSeries:
            self.status = Status.ERROR
            print('Choose series before measuring')
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

    def getSeriesList(self):
        return [*self.series.values()]

    def getSeriesDict(self):
        return self.series
    
    def getStatus(self):
        if not self.worker.isWorikng():
            self.status = Status.NO
        return self.status

    def calculateCH4(self, data):
        return self.currentCalibration.calculateCH4(data)
