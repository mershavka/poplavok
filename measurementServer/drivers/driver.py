import spidev
import smbus2
import bme280
from math import exp
import datetime as dt
from ..common import ValuesNames
from .PCA9685 import PCA9685

class Driver:
    #0x76 - BME280 address (pressure)
    i2c_port = 1	
    bme280_address = 0x76
    pca9685_address = 0x40
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
        #i2c
        self.i2c_bus = smbus2.SMBus(Driver.i2c_port)
        #pca
        self.pca9685 = PCA9685(self.i2c_bus, self.pca9685_address)
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
    

    #LED0 -> Вентилятор 1
    #LED1 -> Вентилятор 2
    def pca_set_fan1(self, value):
        self.pca9685.set_led(0, value)

    def pca_set_fan2(self, value):
        self.pca9685.set_led(1, value)
    
    #LED8 -> Светодиод 1
    def pca_set_first_led(self, value):
        self.pca9685.set_led(8, value)
    
    #LED9 -> Светодиод 2
    def pca_set_second_led(self, value):
        self.pca9685.set_led(9, value)
    
    #LED2 -> Накал сенсора
    def pca_set_heater(self, value):
        self.pca9685.set_led(2, value)


    def pca_control_fan(self, fan_id = 0, dutycycle = 50, delay = 0):
        #id = 0 или 1 (первый или второй вентилятор)
        maxValue = 2**12
        delay_time = round(delay * maxValue / 100, 0)
        led_on_time = round(maxValue * dutycycle / 100, 0)
        led_off_count = delay_time + led_on_time - 1
        on = int(delay_time)
        off = int(0 if led_off_count < 0 else led_off_count)
        print("On: {} / 4096, off : {} / 4096".format(on, off))
        self.pca9685.set_pwm(channel=fan_id, on=int(delay_time), off=int(led_off_count))


    def pca_turn_fans_on(self, fan_id):
        self.pca9685.set_led(0, 1)
        self.pca9685.set_led(1, 1)

    def pca_turn_fans_off(self, fan_id):
        self.pca9685.set_led(0, 0)
        self.pca9685.set_led(1, 0)


    def open(self):
        # self.pca9685.begin()
        self.bme280_calibration_params = bme280.load_calibration_params(self.i2c_bus, Driver.bme280_address)
        self.pca_set_first_led(1) #зажечь первый светодиод
        self.pca_set_second_led(0) #не зажигать второй светодиод
        self.pca_set_heater(1) #включить нагрев сенсора

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
            self.pca_set_second_led(1)
            bme280_data = bme280.sample(self.i2c_bus, Driver.bme280_address, self.bme280_calibration_params)
            value = self.adcGetData()
            self.__lastData[Driver.timeString] = dt.datetime.now()
            self.__lastData[Driver.adcString] = value
            self.__lastData[Driver.voltageString] = value * Driver.adcRange / Driver.adcQuantizationLevels
            self.__lastData[Driver.temperatureString] = bme280_data.temperature
            self.__lastData[Driver.rHumidityString] = bme280_data.humidity
            self.__lastData[Driver.aHumidityString] = Driver.absoluteHumidity(bme280_data.humidity, bme280_data.pressure, bme280_data.temperature)
            self.__lastData[Driver.pressureString] = bme280_data.pressure
            self.pca_set_second_led(0)
            return self.__lastData
