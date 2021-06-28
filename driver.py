class Driver:

	__i2c_port = 1
	__bme280_address = 0x76

	def __init__(self):
		pass

	@property	
	def i2c_port(self):
		return self.__i2c_port

	@i2c_port.setter
	def i2c_port(self, port):
		if port > 0:
			self.__i2c_port = port
		else:
			raise ValueError

	def readData():
		