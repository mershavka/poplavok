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
temperatureString = 'Temperature, °C'
rHumidityString = 'Related Humidity, %'
aHumidityString = 'Absolute Humidity, kg/m^3'
pressureString = 'Pressure, hPa'
ch4String = 'CH4, ppm'

class MeasurementServer:

    testMode = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MeasurementServer, cls).__new__(cls)
        return cls.instance

    def __readFromDevice():
        ms = MeasurementServer()
        if MeasurementServer.testMode:
            return { timeString: dt.datetime.now(),  adcString: 2044,
                         voltageString: 1.2,  resistanceString: 3000, 
                         temperatureString: 25,  rHumidityString: 35, 
                         aHumidityString: 10,  pressureString: 10000,  ch4String: 0}
        return ms.device.readData()

    def __writeToMeasureFile(data):
        ms = MeasurementServer()
        ms.fs.writeToMeasurement(ms.currentMeasurement, data)

    def __init__(self):
        self.series = {}
        # self.device = Driver()
        self.fs = MeasurementFileSystem(EXEC_DIR)
        self.series = self.fs.loadSeries()
        if self.series:
            self.lastSeriesId = max(self.series.keys())
        else:
            self.lastSeriesId = 0
        self.worker = MeasurementModule()
        MeasurementModule.setReadFunc(self.__readFromDevice)
        MeasurementModule.setWriteFunc(self.__writeToMeasureFile)

        # Status variables
        self.status = Status.NO
        self.currentSeries = None
        self.currentMeasurement = None
        self.currentCalibration = None

        self.header = [	 timeString,  adcString,
                         voltageString,  resistanceString, 
                         temperatureString,  rHumidityString, 
                         aHumidityString,  pressureString,  ch4String]


    # def __measurementsThreadFunc(self, fileName, duration, periodicity, calibrationPath):
    #     try:
    #         expStart = time.time()
    #         dr = Driver()
    #         if (dr.open() < 0):
    #             raise BoardConnectionError

    #         appendRowToCsv(fileName, self.header)
    #         timing = 0

    #         while time.time() - expStart <= duration:
    #             if self.stopingEvent.is_set():
    #                 break
    #             if time.time() - timing >= periodicity:
    #                 timing = time.time()
    #                 dataDictionary = dr.readData()
    #                 newRow = ['{:%Y/%m/%d %H:%M:%S.%f}'.format(dataDictionary[Driver.timeString]), dataDictionary[Driver.adcString], \
    #                         round(dataDictionary[Driver.voltageString], 3), round(dataDictionary[Driver.resistanceString], 1), \
    #                         round(dataDictionary[Driver.temperatureString], 2), round(dataDictionary[Driver.rHumidityString], 2), round(dataDictionary[Driver.aHumidityString], 5),round(dataDictionary[Driver.pressureString], 2)]
    #                 if calibrationPath != None:
    #                     #Здесь нужно считать результат калибровки и рассчитывать ppm метана
    #                     ch4 = 0
    #                     newRow.append(ch4)
    #                     print("CH4, ppm: {}".format(ch4), end= " ")
    #                 print("Time: {}, ADC value: {}, Voltage: {:.3f}, Resistance: {:.1f}, Temperature: {:.2f}, RHumidity: {:.2f}, AHumidity: {:.4f} ,Pressure: {:.2f}".format(*newRow))
    #                 appendRowToCsv(fileName, newRow)
    #         self.status = Status.NO
    #     except BoardConnectionError:
    #         print('Connection to Board FAILED!!! Please, check board connection with Raspberry Pi.')
    #         self.status = Status.ERROR
    #     except Exception as e:
    #         traceback.print_exc()
    #         self.status = Status.ERROR
    #         return -1
    #     finally:
    #         dr = None
    #     return 0

    # def runMeasurementsThread(self, duration, periodicity, calibrationPath):
    #     if self.currentSeries is None:
    #         return None
    #     self.currentMeasurementFile = self.currentSeries.dir_path + '/exp_{:%Y_%m_%d_%H%M%S}.csv'.format(dt.datetime.now())
    #     self.th0 = Thread(target=self.__measurementsThreadFunc, args=(duration, periodicity, None))

    # def startMeasurements(self, duration, periodicity):
    #     self.th0 = Thread(target=self.__measurementsThreadFunc, args=(duration, periodicity, None))
    #     self.status = Status.COMMON_EXPERIMENT
    #     self.th0.start()

    # def startExperiment(self, duration=600, periodicity = 2, calibrationPath = None):
    #     self.stopingEvent.clear()
    #     if calibrationPath is None:
    #         print('No calibration file')
    #         self.status = Status.ERROR
    #     else:
    #         if filePath is None:
    #             print('No file name for saving experiment')
    #             filePath = ('exp_{:%Y_%m_%d_%H%M%S}.csv').format(dt.datetime.now())

    #         self.status = Status.FIELD_EXPERIMENT
    #         self.th = Thread(target=self.__measurementsThreadFunc, args=(duration, periodicity, calibrationPath))
    #         self.th.start()

    # def __runCal1Experiment(self, filePath=None, duration=600, periodicity = 2):
    #         self.th1 = Thread(target=self.__measurementsThreadFunc, args=(duration, periodicity, None))
    #         self.th1.start()

    # def startCal1Experiment(self, filePath, duration, periodicity):
    #     self.stopingEvent.clear()
    #     self.__runCal1Experiment(filePath, duration, periodicity)		

    # def startCal2Experiment(self, dataFilePathes, cal1FilePath):
    #     self.stopingEvent.clear()
    #     pass

    # def startCalibrationStep1(self, filePathes, resultPath = None):
    #     self.status = Status.CALIBRATION_1
    #     resultPath = (resultPath, 'step1_{:%Y_%m_%d_%H%M%S}.csv'.format(dt.datetime.now()))[resultPath is None]
    #     step1 = CalibrationModule()
    #     step1.calibrateFirstStep(filePathes, resultPath)

    # def startCalibrationStep2(self, dirPath, step1resultPath, resultPath = None):
    #     self.status = Status.CALIBRATION_2
    #     if step1resultPath is None:
    #         print('No file with model from first step')
    #         self.status = Status.ERROR
    #         return -1
    #     resultPath = (resultPath, 'step1_{:%Y_%m_%d_%H%M%S}.csv'.format(dt.datetime.now()))[resultPath is None]
    #     step2 = CalibrationModule()
    #     step2.calibrateSecondStep(dirPath, resultPath)
    #     bestModel = step2.bestModel()
    #     return 

    # def stopExperiment(self):
    #     if self.th0.is_alive():
    #         self.stopingEvent.set()
    #     self.status = Status.NO

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
        self.worker.startMeasurement(new_measurement)
        self.status = Status.COMMON_EXPERIMENT

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
            

