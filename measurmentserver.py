from driver import Driver
import datetime as dt
import time
import csv
import traceback
from series import Series
from threading import Thread, Event
from callibration import CalibrationModule
import glob, os
from measurementfilesystem import MeasurementFileSystem
from enums import MeasureType, Status

EXEC_DIR = "/home/pi/Documents/Repos/poplavok-algorithm/MServer"

def appendRowToCsv(filename, listOfElements):
    with open(filename, 'a+', newline ='') as writeObj:
        writer = csv.writer(writeObj)
        writer.writerow(listOfElements)

class Error(Exception):
    """Base class for other exceptions"""
    pass

class BoardConnectionError(Error):
    pass

class FilePathError(Error):
    pass

class MeasurementServer:

    def __init__(self):
        self.fileSystem = MeasurementFileSystem(EXEC_DIR)
        self.status = Status.NO
        self.currentSeries = None

        self.lastData = {}
        self.stopingEvent = Event()
        self.header = [	Driver.timeString, Driver.adcString,
                        Driver.voltageString, Driver.resistanceString, 
                        Driver.temperatureString, Driver.rHumidityString, 
                        Driver.aHumidityString, Driver.pressureString, Driver.ch4String]


    def __measurementsThreadFunc(self, fileName, duration, periodicity, calibrationPath):
        try:
            expStart = time.time()
            dr = Driver()
            if (dr.open() < 0):
                raise BoardConnectionError

            appendRowToCsv(fileName, self.header)
            timing = 0

            while time.time() - expStart <= duration:
                if self.stopingEvent.is_set():
                    break
                if time.time() - timing >= periodicity:
                    timing = time.time()
                    dataDictionary = dr.readData()
                    newRow = ['{:%Y/%m/%d %H:%M:%S.%f}'.format(dataDictionary[Driver.timeString]), dataDictionary[Driver.adcString], \
                            round(dataDictionary[Driver.voltageString], 3), round(dataDictionary[Driver.resistanceString], 1), \
                            round(dataDictionary[Driver.temperatureString], 2), round(dataDictionary[Driver.rHumidityString], 2), round(dataDictionary[Driver.aHumidityString], 5),round(dataDictionary[Driver.pressureString], 2)]
                    if calibrationPath != None:
                        #Здесь нужно считать результат калибровки и рассчитывать ppm метана
                        ch4 = 0
                        newRow.append(ch4)
                        print("CH4, ppm: {}".format(ch4), end= " ")
                    print("Time: {}, ADC value: {}, Voltage: {:.3f}, Resistance: {:.1f}, Temperature: {:.2f}, RHumidity: {:.2f}, AHumidity: {:.4f} ,Pressure: {:.2f}".format(*newRow))
                    appendRowToCsv(fileName, newRow)
            self.status = Status.NO
        except BoardConnectionError:
            print('Connection to Board FAILED!!! Please, check board connection with Raspberry Pi.')
            self.status = Status.ERROR
        except Exception as e:
            traceback.print_exc()
            self.status = Status.ERROR
            return -1
        finally:
            dr = None
        return 0

    def runMeasurementsThread(self, duration, periodicity, calibrationPath):
        if self.currentSeries is None:
            return None
        self.currentMeasurementFile = self.currentSeries.dir_path + '/exp_{:%Y_%m_%d_%H%M%S}.csv'.format(dt.datetime.now())
        self.th0 = Thread(target=self.__measurementsThreadFunc, args=(duration, periodicity, None))

    def startMeasurements(self, duration, periodicity):
        self.th0 = Thread(target=self.__measurementsThreadFunc, args=(duration, periodicity, None))
        self.status = Status.COMMON_EXPERIMENT
        self.th0.start()

    def startExperiment(self, duration=600, periodicity = 2, calibrationPath = None):
        self.stopingEvent.clear()
        if calibrationPath is None:
            print('No calibration file')
            self.status = Status.ERROR
        else:
            if filePath is None:
                print('No file name for saving experiment')
                filePath = ('exp_{:%Y_%m_%d_%H%M%S}.csv').format(dt.datetime.now())

            self.status = Status.FIELD_EXPERIMENT
            self.th = Thread(target=self.__measurementsThreadFunc, args=(duration, periodicity, calibrationPath))
            self.th.start()

    def __runCal1Experiment(self, filePath=None, duration=600, periodicity = 2):
            self.th1 = Thread(target=self.__measurementsThreadFunc, args=(duration, periodicity, None))
            self.th1.start()

    def startCal1Experiment(self, filePath, duration, periodicity):
        self.stopingEvent.clear()
        self.__runCal1Experiment(filePath, duration, periodicity)		

    def startCal2Experiment(self, dataFilePathes, cal1FilePath):
        self.stopingEvent.clear()
        pass

    def startCalibrationStep1(self, filePathes, resultPath = None):
        self.status = Status.CALIBRATION_1
        resultPath = (resultPath, 'step1_{:%Y_%m_%d_%H%M%S}.csv'.format(dt.datetime.now()))[resultPath is None]
        step1 = CalibrationModule()
        step1.calibrateFirstStep(filePathes, resultPath)

    def startCalibrationStep2(self, dirPath, step1resultPath, resultPath = None):
        self.status = Status.CALIBRATION_2
        if step1resultPath is None:
            print('No file with model from first step')
            self.status = Status.ERROR
            return -1
        resultPath = (resultPath, 'step1_{:%Y_%m_%d_%H%M%S}.csv'.format(dt.datetime.now()))[resultPath is None]
        step2 = CalibrationModule()
        step2.calibrateSecondStep(dirPath, resultPath)
        bestModel = step2.bestModel()
        return 

    def stopExperiment(self):
        if self.th0.is_alive():
            self.stopingEvent.set()
        self.status = Status.NO

    def createSeries(self, description="", type=Series.SeriesType.COMMON):		
        new_series = Series(path=EXEC_DIR, id=self.seriesNextId, description=description, type=type)
        self.fileSystem.addSeries(new_series)
        self.seriesNextId += 1
        return new_series

    def chooseSeries(self, id):
        self.currentSeries = self.fileSystem.getSeriesById(id)
        if self.currentSeries is None:
            self.status = Status.ERROR
            print("No series with id={}".format(id))		

    def getListSeries(self):
        # Какой интерфейс?? Кто будет читать это и как?
        return self.fileSystem.getSeriesList()
