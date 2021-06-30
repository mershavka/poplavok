import datetime as dt
import time
import csv
from driver import Driver
import traceback
from threading import Thread

def appendRowToCsv(filename, listOfElements):
	with open(filename, 'a+', newline ='') as writeObj:
		writer = csv.writer(writeObj)
		writer.writerow(listOfElements)

def runMeasurements(file_name, duration, periodicity, calibrationPath=None):
	try:
		expStart = time.time()
		dr = Driver()
		if (dr.open() < 0):
			print('Connection to Board FAILED!!! Please, check board connection with Raspberry Pi.')
			raise Exception

		appendRowToCsv(file_name, ['Time','ADC value','Voltage, V', 'Resistance, Om', 'Temperature,°C', 'Humidity, % RH', 'Pressure, hPa,', 'CH4, ppm'])
		timing = 0

		while time.time() - expStart <= duration:
			if time.time() - timing >= periodicity:
				timing = time.time()
				dataDictionary = dr.readData()
				newRow = ['{:%Y/%m/%d %H:%M:%S.%f}'.format(dataDictionary[Driver.timeString]), dataDictionary[Driver.adcString], \
						round(dataDictionary[Driver.voltageString], 3), round(dataDictionary[Driver.resistanceString], 1), \
						round(dataDictionary[Driver.temperatureString], 2), round(dataDictionary[Driver.humidityString], 2), round(dataDictionary[Driver.pressureString], 2)]
				if calibrationPath != None:
					ch4 = 0
					newRow.append(ch4)
					print("CH4, ppm: {}".format(ch4), end= " ")
				print("Time: {}, ADC value: {}, Voltage: {:.3f}, Resistance: {:.1f}, Temperature: {:.2f}, Humidity: {:.2f}, Pressure: {:.2f}".format(*newRow))
				appendRowToCsv(file_name, newRow)
	except Exception as e:
		traceback.print_exc()
		return -1
	finally:
		dr = None
	return 0

def runExperiment(filePath, duration, periodicity, calibrationPath=None):
	file_name = ('exp_{:%Y_%m_%d_%H%M%S}.csv').format(dt.datetime.now())
	th = Thread(target=runMeasurements, args=(file_name, 1000, 1))
	th.start()

	for i in range(5):
		print(f"from main thread: {i}")
		time.sleep(1)

def runExpCal1():
	pass

def runExpCal2():
	pass