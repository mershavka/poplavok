import datetime as dt
import time
import csv
from driver import Driver
from threading import Thread

def appendRowToCsv(filename, listOfElements):
	with open(filename, 'a+', newline ='') as writeObj:
		writer = csv.writer(writeObj)
		writer.writerow(listOfElements)

def runExperiment(duration, periodicity, mode=0):
	try:
		expStart = time.time()
		dr = Driver()
		if (dr.open() < 0):
			print('Не удалось установить соединение с железом. Проверьте, подключена ли измерительная плата к Raspberry Pi.')
			raise Exception

		file_name = ('exp_{:%Y_%m_%d_%H%M%S}.csv').format(dt.datetime.now())
		appendRowToCsv(file_name, ['Time','ADC value','Voltage, V', 'Resistance, Om', 'Temperature,°C', 'Humidity, % RH', 'Pressure, hPa,', 'CH4, ppm'])

		while time.time() - expStart <= duration:
				if time.time() - timing >= periodicity:
					timing = time.time()
					dataDictionary = dr.readData()
					newRow = ['{:%Y/%m/%d %H:%M:%S.%f}'.format(dataDictionary[Driver.timeString]), dataDictionary[Driver.adcString], \
							round(dataDictionary[Driver.voltageString], 3), round(dataDictionary[Driver.resistanceString], 1), \
							round(dataDictionary[Driver.temperatureString], 2), round(dataDictionary[Driver.humidityString], 2), round(dataDictionary[Driver.pressureString], 2)]
					if mode != 0:
						ch4 = 0
						newRow.append(ch4)
						print("CH4, ppm: {}".format(ch4), end= " ")
					print("Time: {}, ADC value: {}, Voltage: {:.3f}, Resistance: {:.1f}, Temperature: {:.2f}, Humidity: {:.2f}, Pressure: {:.2f}".format(*newRow))
					appendRowToCsv(file_name, newRow)
	except Exception:
		return -1
	finally:
		dr = None
	return 0

th = Thread(target=runExperiment(1000, 1))
th.start()

for i in range(5):
    print(f"from main thread: {i}")
    time.sleep(1)