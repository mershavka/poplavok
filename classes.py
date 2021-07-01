import enum
from math import sqrt
from numpy.core.fromnumeric import nonzero
from scipy.optimize import curve_fit
import numpy as np
from enum import Enum
from main import appendRowToCsv
from driver import Driver
import datetime as dt
import time
import csv
import traceback
from threading import Thread, Event

class Model_fitting:

	def __init__(self,  dependence_function, predictors, dependent_variable, variable_name = 'undefined'):
		 self.variable_name = variable_name
		 self.X = predictors
		 self.y = dependent_variable
		 self.function = dependence_function
		 self.__fit()

	def display_info(self):
		print('Это модель для параметра "{}"'.format(self.variable_name))

	def __fit(self):

		self.popt, self.pcov = curve_fit(self.function, self.X, self.y)
		#Количество предикторов (независимых переменных)
		self.predictors_count = np.ndim(self.X)
		self.y_hat = self.function(self.X, *self.popt)
		#Residual sum of squares (сумма квадратов остатков)
		self.ss_residual = sum((self.y-self.y_hat)**2)
		 #Total sum of squares (общая сумма квадратов)
		self.ss_total = sum((self.y-np.mean(self.y))**2)
		#Коэффициент детерминации — R-квадрат  
		self.r_squared = 1 - (float(self.ss_residual))/self.ss_total
		#Скорректированный коэффициент детерминации (adjusted)
		self.adjusted_r_squared = 1 - (1-self.r_squared)*(len(self.y)-1)/(len(self.y)-self.predictors_count)
		#Root Mean Square Error Среднеквадратическая ошибка модели
		self.rmse = sqrt(self.ss_residual / len(self.y))

class CalibrationModule:
	pass

class Status(enum.Enum):
		NO = (0, "Nothing is happening")
		ERROR = (1, "Error occured")
		FIELD_EXPERIMENT = (2, "Callibrated experiment is underway")
		CALIBRATION_1 = (3, "Experiment for calibration (first step) is underway")
		CALIBRATION_2 = (4, "Experiment for calibration (second step) is underway")
		WARNING = (5, "Warning")
		def __init__(self, id, title):
			self.id = id
			self.title = title
		def info(self):
			print("Name - %s, id - %s, desription - %s"%(self.name, self.id, self.title))

class Error(Exception):
	"""Base class for other exceptions"""
	pass

class BoardConnectionError(Error):
	pass

class FilePathError(Error):
	pass
	
class MeasurementServer:

	def __new__(cls, data=None):
		if data is None:
			print('Error while creating class MeasurementServer')
			return None
		else:
			return super().__new__(cls)

	def __init__(self):
		self.status = Status.NO
		self.lastData = {}
		self.stopingEvent = Event()
		self.header = ['Time','ADC value','Voltage, V', 'Resistance, Om', 'Temperature,°C', 'Humidity, % RH', 'Pressure, hPa,', 'CH4, ppm']

	def __runMeasurements(self, fileName, duration, periodicity, calibrationPath):
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
							round(dataDictionary[Driver.temperatureString], 2), round(dataDictionary[Driver.humidityString], 2), round(dataDictionary[Driver.pressureString], 2)]
					if calibrationPath != None:
						#Здесь нужно считать результат калибровки и рассчитывать ppm метана
						ch4 = 0
						newRow.append(ch4)
						print("CH4, ppm: {}".format(ch4), end= " ")
					print("Time: {}, ADC value: {}, Voltage: {:.3f}, Resistance: {:.1f}, Temperature: {:.2f}, Humidity: {:.2f}, Pressure: {:.2f}".format(*newRow))
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

	def startMeasurements(self, filePath, duration, periodicity):
		self.th0 = Thread(target=self.__runMeasurements, args=(filePath, duration, periodicity, None))
		self.th0.start()

	def __runExperiment(self, filePath, duration, periodicity, calibrationPath):
		self.th = Thread(target=self.__runMeasurements, args=(filePath, duration, periodicity, calibrationPath))
		self.th.start()

		for i in range(5):
			print(f"from main thread: {i}")
			time.sleep(1)

	def startExperiment(self, filePath=None, duration=600, periodicity = 2, calibrationPath = None):
		self.stopingEvent.clear()
		if calibrationPath is None:
			print('No calibration file')
			self.status = Status.ERROR
		else:
			if filePath is None:
				print('No file name for saving experiment')
				filePath = ('exp_{:%Y_%m_%d_%H%M%S}.csv').format(dt.datetime.now())

			self.status = Status.FIELD_EXPERIMENT
			self.__runExperiment(filePath, duration, periodicity, calibrationPath)

	def __runCal1Experiment(self, filePath=None, duration=600, periodicity = 2):
			self.th1 = Thread(target=self.__runMeasurements, args=(filePath, duration, periodicity, None))
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

	def startCalibrationStep2(self, filePathes, step1resultPath, resultPath = None):
		self.status = Status.CALIBRATION_2
		if step1resultPath is None:
			print('No file with model from first step')
			self.status = Status.ERROR
			return -1
		resultPath = (resultPath, 'step1_{:%Y_%m_%d_%H%M%S}.csv'.format(dt.datetime.now()))[resultPath is None]
		step2 = CalibrationModule()
		step2.calibrateSecondStep(filePathes, resultPath)
		bestModel = step2.bestModel()
		return 

	def stopExperiment(self):
		if self.th.is_alive():
			self.stopingEvent.set()
		self.status = Status.NO
