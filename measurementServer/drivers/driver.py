import spidev
import smbus2
import bme280
from math import exp
import datetime as dt
from ..common import ValuesNames

class Driver:
    #0x76 - BME280 address (pressure)
    i2c_port = 1	
    bme280_address = 0x76
    adcRange = 2.5 #V
    adcQuantizationLevels = 2**16
    RL = 3*10**3
    const2 = 1.024

    timeString 			= ValuesNames.timestamp.name
    adcString 			= ValuesNames.adc.name
    voltageString 		= ValuesNames.voltage.name
    temperatureString 	= ValuesNames.temperature.name
    rHumidityString		= ValuesNames.rHumidity.name
    aHumidityString 	= ValuesNames.aHumidity.name
    pressureString 		= ValuesNames.pressure.name

    #0x2a - AmbiMate Sensor Module address (CO2)
    ambimate_addres = 0x2a
    statusHighByte = 0x00
    temperatureHighByte = 0x01
    humidityHighByte = 0x03
    eCO2HighByte = 0x0B
    VOCHighByte = 0x0D
    optionalSensorByte = 0x82
    scanStartByte = 0xC0
            
    def __init__(self):
        #bme280
        self.i2c_bus = smbus2.SMBus(Driver.i2c_port)
        #spi
        self.spi = spidev.SpiDev()
        self.__lastData = dict.fromkeys([Driver.timeString, Driver.adcString, Driver.voltageString, Driver.temperatureString, Driver.rHumidityString, Driver.aHumidityString, Driver.pressureString])


    def adcGetData(self):
        adcData = str()
        rxData = self.spi.xfer([0x00, 0x00, 0x00]) #Функция осуществления SPI транзакции, list of values – непосредственно передаваемые данные, функция возвращает данные, принятые от подчиненного устройства.
        for i in rxData:
            adcData += bin(i)[2:].zfill(8)
        adcData = adcData[6:22]
        adcValue = int(adcData,2)
        return adcValue

    def open(self):
        self.bme280_calibration_params = bme280.load_calibration_params(self.i2c_bus, Driver.bme280_address)

        self.spi.open(0,0) #модуль и сигнал Chip Select, SPI0 и SPI0_CE0_N
        self.spi.lsbfirst = False
        self.spi.cshigh = True #в активном режиме сигнал на выходе Chip Select высокий
        self.spi.mode = 0b00 #исходный уровень сигнала синхронизации – низкий, по переднему фронту происходит выборка данных, по заднему – установка.
        self.spi.bits_per_word = 8
        self.spi.max_speed_hz = 1000

    def absoluteHumidity(RH = 40, hPa = 1013.25, t = 20):
        #RH [%], P[гПa], t[C]
        Rv = 461.5 # газовая постоянная для водяного пара [Дж/(кг*K)]
        ew = 6.112 * exp(17.62 * t / (243.12 + t)) * (1.0016 + 3.15e-6 * hPa - 0.074 / hPa) # [гПа]
        T = t + 273.15 #[K]
        AH = RH * ew / Rv / T #кг/м^3
        return AH

    def readData(self):
            bme280_data = bme280.sample(self.i2c_bus, Driver.bme280_address, self.bme280_calibration_params)
            value = self.adcGetData()
            self.__lastData[Driver.timeString] = dt.datetime.now()
            self.__lastData[Driver.adcString] = value
            self.__lastData[Driver.voltageString] = value * Driver.adcRange / Driver.adcQuantizationLevels
            self.__lastData[Driver.temperatureString] = bme280_data.temperature
            self.__lastData[Driver.rHumidityString] = bme280_data.humidity
            self.__lastData[Driver.aHumidityString] = Driver.absoluteHumidity(bme280_data.humidity, bme280_data.pressure, bme280_data.temperature)
            self.__lastData[Driver.pressureString] = bme280_data.pressure
            return self.__lastData
