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
    
    def pca_init(self):
        mode1_addr = 0x00
        mode1_value = 0x01 # Disable Sleep Mode to Enable LEDs
        self.i2c_bus.write_byte_data(Driver.pca9685_address, mode1_addr, mode1_value)
        ALL_LED_ON_L_addr  = 0xFA
        ALL_LED_ON_H_addr  = 0xFB
        ALL_LED_OFF_L_addr = 0xFC
        ALL_LED_OFF_H_addr = 0xFD
        self.i2c_bus.write_byte_data(Driver.pca9685_address, ALL_LED_ON_L_addr, 0x00)
        self.i2c_bus.write_byte_data(Driver.pca9685_address, ALL_LED_ON_H_addr, 0x00)
        self.i2c_bus.write_byte_data(Driver.pca9685_address, ALL_LED_OFF_L_addr, 0x00)
        self.i2c_bus.write_byte_data(Driver.pca9685_address, ALL_LED_OFF_H_addr, 0x10)
    
    def pca_set_led8(self, value):
        LED8_ON_L_addr  = 0x26
        LED8_ON_H_addr  = 0x27
        LED8_OFF_L_addr = 0x28
        LED8_OFF_H_addr = 0x29
        self.i2c_bus.write_byte_data(Driver.pca9685_address, LED8_ON_L_addr, 0x00)
        self.i2c_bus.write_byte_data(Driver.pca9685_address, LED8_ON_H_addr, 0x10 if value else 0x00)
        self.i2c_bus.write_byte_data(Driver.pca9685_address, LED8_OFF_L_addr, 0x00)
        self.i2c_bus.write_byte_data(Driver.pca9685_address, LED8_OFF_H_addr, 0x00 if value else 0x10)
    
    def pca_set_led9(self, value):
        LED9_ON_L_addr  = 0x2A
        LED9_ON_H_addr  = 0x2B
        LED9_OFF_L_addr = 0x2C
        LED9_OFF_H_addr = 0x2D
        self.i2c_bus.write_byte_data(Driver.pca9685_address, LED9_ON_L_addr, 0x00)
        self.i2c_bus.write_byte_data(Driver.pca9685_address, LED9_ON_H_addr, 0x10 if value else 0x00)
        self.i2c_bus.write_byte_data(Driver.pca9685_address, LED9_OFF_L_addr, 0x00)
        self.i2c_bus.write_byte_data(Driver.pca9685_address, LED9_OFF_H_addr, 0x00 if value else 0x10)
    
    def pca_set_heater(self, value):
        LED2_ON_L_addr  = 0x0E
        LED2_ON_H_addr  = 0x0F
        LED2_OFF_L_addr = 0x10
        LED2_OFF_H_addr = 0x11
        self.i2c_bus.write_byte_data(Driver.pca9685_address, LED2_ON_L_addr, 0x00)
        self.i2c_bus.write_byte_data(Driver.pca9685_address, LED2_ON_H_addr, 0x10 if value else 0x00)
        self.i2c_bus.write_byte_data(Driver.pca9685_address, LED2_OFF_L_addr, 0x00)
        self.i2c_bus.write_byte_data(Driver.pca9685_address, LED2_OFF_H_addr, 0x00 if value else 0x10)

    def set_pwm(self, channel, on, off):
        """Sets a single PWM channel."""
        LED0_ON_L_addr  = 0x06
        LED0_ON_H_addr  = 0x07
        LED0_OFF_L_addr = 0x08
        LED0_OFF_H_addr = 0x09
        #channel — Один из выводов PWM от 0 до 15
        #on — В какой момент цикла из 4096 частей включить ШИМ
        #off — В какой момент цикла из 4096 частей выключить ШИМ
        self.i2cBus.write_byte_data(self.address, LED0_ON_L_addr + 4 * channel, on & 0xFF)
        self.i2cBus.write_byte_data(self.address, LED0_ON_H_addr + 4 * channel, (on & 0xF00) >> 8)
        self.i2cBus.write_byte_data(self.address, LED0_OFF_L_addr + 4 * channel, off & 0xFF)
        self.i2cBus.write_byte_data(self.address, LED0_OFF_H_addr + 4 * channel, (off & 0xF00) >> 8)

    def pca_control_fan(self, fan_id = 0, dutycycle = 50, delay = 0):
        #id = 0 или 1 (первый или второй вентилятор)
        maxValue = 2**12
        delay_time = round(delay * maxValue / 100, 0)
        led_on_time = round(maxValue * dutycycle / 100, 0)
        led_off_count = delay_time + led_on_time - 1
        self.set_pwm(channel=fan_id, on=delay_time, off=led_off_count)


    def open(self):
        self.pca_init()
        self.bme280_calibration_params = bme280.load_calibration_params(self.i2c_bus, Driver.bme280_address)
        self.pca_set_led8(1)
        self.pca_set_led9(0)
        self.pca_set_heater(1)

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
            self.pca_set_led9(1)
            bme280_data = bme280.sample(self.i2c_bus, Driver.bme280_address, self.bme280_calibration_params)
            value = self.adcGetData()
            self.__lastData[Driver.timeString] = dt.datetime.now()
            self.__lastData[Driver.adcString] = value
            self.__lastData[Driver.voltageString] = value * Driver.adcRange / Driver.adcQuantizationLevels
            self.__lastData[Driver.temperatureString] = bme280_data.temperature
            self.__lastData[Driver.rHumidityString] = bme280_data.humidity
            self.__lastData[Driver.aHumidityString] = Driver.absoluteHumidity(bme280_data.humidity, bme280_data.pressure, bme280_data.temperature)
            self.__lastData[Driver.pressureString] = bme280_data.pressure
            self.pca_set_led9(0)
            return self.__lastData
