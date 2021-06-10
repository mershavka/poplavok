from smbus import SMBus
import struct

bus = SMBus(1)
data = bus.read_i2c_block_data(0x2a, 0x01, 2)


print(bytearray(data))
data = struct.unpack('<e',bytearray(data))
print(data)
bus.close()

