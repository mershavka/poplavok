import datetime as dt
import time
import csv

import spidev
import smbus2
import bme280

#i2c settings
i2c_port = 1
bme280_address = 0x76

#experimnet settings
timing = 0
period = 5

#functions
def appendRowToCsv(filename, listOfElements):
    with open(filename, 'a+', newline ='') as writeObj:
        writer = csv.writer(writeObj)
        writer.writerow(listOfElements)

def adcGetData():
    adcData = str()
    rxData = spi.xfer([0x00, 0x00, 0x00])
    for i in rxData:
        adcData += bin(i)[2:].zfill(8)
    adcData = adcData[6:22]
    adcValue = int(adcData,2)
    return adcValue


def runExperiment(duration, periodicity, mode):
	
	return 0

try:
    #bme280
    i2c_bus = smbus2.SMBus(i2c_port)
    bme280_calibration_params = bme280.load_calibration_params(i2c_bus, bme280_address)
    #spi
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.lsbfirst = False
    spi.cshigh = True
    spi.mode = 0b00
    spi.bits_per_word = 8
    spi.max_speed_hz = 1000

    file_name = ('exp_{:%Y_%m_%d_%H%M%S}.csv').format(dt.datetime.now())
    appendRowToCsv(file_name, ['Time','ADC value','Voltage, V', 'Resistance, Om', 'Temperature,°C', 'Humidity, % RH', 'Pressure, hPa'])

    while True:
        if time.time() - timing > period:
            timing = time.time()
            #read data from bme280
            bme280_data = bme280.sample(i2c_bus, bme280_address, bme280_calibration_params)

            value = adcGetData()
            voltage = value * 2.5 / 2**16
            resistance = 3*10**3 * 1.024/ (voltage - 1.024)
            newRow = ['{:%Y/%m/%d %H:%M:%S.%f}'.format(dt.datetime.now()), value, round(voltage, 3), round(resistance, 1), round(bme280_data.temperature, 2), round(bme280_data.humidity, 2), round(bme280_data.pressure, 2)]
            print("Time: {}, ADC value: {}, Voltage: {:.3f}, Resistance: {:.1f}, Temperature: {:.2f}, Humidity: {:.2f}, Pressure: {:.2f}".format(*newRow))
            appendRowToCsv(file_name, newRow)

finally:
    spi.close()
    i2c_bus.close()