from smbus2 import SMBus, i2c_msg
import struct
import time
#Data SDA changes only when SCL == 0, except: 1) master initiates START (during SCL > 0, Master changes SDA from 1 to 0), slaves start listening
#2) master initiates STOP (during SCL > 0, Master changes SDA from 0 to 1)
#After every byte receiver answers with bit 0 (A - acknowledgment), if receiver doesn't get byte, bit is set to 1 (N - negative acknowledgment)

#Trancemission: S(start),[Adr(write to this device), 0(write)],A,[Byte_1],A,...[Byte_n],A,P(stop) #A is set by Slave, Bytes are set by Master, Adr = 7 bits
#Receiving: S(start),[Adr(read from this device), 1(read)],A,[Byte_1],A,...[Byte_n],N (to stop Slave at last byte),P(stop) #A is set by Master, Bytes are set by Slave

#0x2a - AmbiMate Sensor Module addres (CO2)
#0x76 - Pressure addres BME280 addres (pressure)
hostAdress = 0x2a
statusHighByte = 0x00
temperatureHighByte = 0x01
humidityHighByte = 0x03
eCO2HighByte = 0x0B
VOCHighByte = 0x0D
optionalSensorByte = 0x82
scanStartByte = 0xC0



try:
    while True:
        with SMBus(1) as bus :
            data = []
            bus.write_byte_data(hostAdress, scanStartByte, 0x7F)            
            for i in range(4):
                bus.write_byte(hostAdress, temperatureHighByte + i)
                data.append(bus.read_byte(hostAdress))            
            #b = bus.read_byte(hostAdress, temperatureHighByte)
            #data = bus.read_i2c_block_data(hostAdress, temperatureHighByte, 4)
            print(data)
            temp = float(data[0] * 256 + data[1]) / 10.0
            hum = float(data[2] * 256 + data[3]) / 10.0
            print(temp, hum)
            time.sleep(3)
            exit
finally:
    bus.close()

