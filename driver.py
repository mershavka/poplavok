import spidev
import smbus2
import bme280
from math import exp
import datetime as dt

class Driver:
    #0x76 - BME280 address (pressure)
    i2c_port = 1	
    bme280_address = 0x76
    adcRange = 2.5 #V
    adcQuantizationLevels = 2**16
    RL = 3*10**3
    const2 = 1.024

    timeString = 'Time'
    adcString = 'ADC value'
    voltageString = 'Voltage, V'
    resistanceString = 'Resistance, Om'
    temperatureString = 'Temperature, °C'
    rHumidityString = 'Related Humidity, %'
    aHumidityString = 'Absolute Humidity, kg/m^3'
    pressureString = 'Pressure, hPa'
    ch4String = 'CH4, ppm'

    #0x2a - AmbiMate Sensor Module address (CO2)
    ambimate_addres = 0x2a
    statusHighByte = 0x00
    temperatureHighByte = 0x01
    humidityHighByte = 0x03
    eCO2HighByte = 0x0B
    VOCHighByte = 0x0D
    optionalSensorByte = 0x82
    scanStartByte = 0xC0

    #конструктор, метод __new__ срабатывает до __init__

    # def __new__(cls, data=None):
    # 	if data is None:
    # 		print('Error')
    # 		return None
    # 	else:
    # 		return super().__new__(cls)
            
    def __init__(self):
        #bme280
        self.i2c_bus = smbus2.SMBus(Driver.i2c_port)
        #spi
        self.spi = spidev.SpiDev()
        self.__lastReceivedData = dict.fromkeys([Driver.timeString, Driver.adcString, Driver.voltageString, Driver.resistanceString, Driver.temperatureString, Driver.rHumidityString, Driver.aHumidityString, Driver.pressureString])


    def adcGetData(self):
        adcData = str()
        rxData = self.spi.xfer([0x00, 0x00, 0x00]) #Функция осуществления SPI транзакции, list of values – непосредственно передаваемые данные, функция возвращает данные, принятые от подчиненного устройства.
        for i in rxData:
            adcData += bin(i)[2:].zfill(8)
        adcData = adcData[6:22]
        adcValue = int(adcData,2)
        return adcValue

    def open(self):
        try:
            self.bme280_calibration_params = bme280.load_calibration_params(self.i2c_bus, Driver.bme280_address)

            self.spi.open(0,0) #модуль и сигнал Chip Select, SPI0 и SPI0_CE0_N
            self.spi.lsbfirst = False
            self.spi.cshigh = True #в активном режиме сигнал на выходе Chip Select высокий
            self.spi.mode = 0b00 #исходный уровень сигнала синхронизации – низкий, по переднему фронту происходит выборка данных, по заднему – установка.
            self.spi.bits_per_word = 8
            self.spi.max_speed_hz = 1000
        except Exception:
            return -1
        return 0

    def absoluteHumidity(RH, P, t):	
        Rv = 461.5 # J/(kg*K)
        ew = 6.112 * exp(17.62 * t / (243.12 + t)) * (1.0016 + 3.15e-6 * P - 0.074 / P) # Pa
        T = t + 273.15
        AH = RH * ew / Rv / T
        return AH

    def readData(self):
            bme280_data = bme280.sample(self.i2c_bus, Driver.bme280_address, self.bme280_calibration_params)
            value = self.adcGetData()
            self.__lastReceivedData[Driver.timeString] = dt.datetime.now()
            self.__lastReceivedData[Driver.adcString] = value
            self.__lastReceivedData[Driver.voltageString] = value * Driver.adcRange / Driver.adcQuantizationLevels
            self.__lastReceivedData[Driver.resistanceString] = Driver.RL * Driver.const2 / (self.__lastReceivedData[Driver.voltageString] - Driver.const2)
            self.__lastReceivedData[Driver.temperatureString] = bme280_data.temperature
            self.__lastReceivedData[Driver.rHumidityString] = bme280_data.humidity
            self.__lastReceivedData[Driver.aHumidityString] = Driver.absoluteHumidity(bme280_data.humidity, bme280_data.pressure, bme280_data.temperature)
            self.__lastReceivedData[Driver.pressureString] = bme280_data.pressure
            return self.__lastReceivedData

    def getDataList(self):
        dataList = []
        return dataList

    def fanOn(self):
        pass

    def fanOff(self):
        pass
