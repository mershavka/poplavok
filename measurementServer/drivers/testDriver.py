from math import exp
import datetime as dt
from ..common import ValuesNames

class TestDriver:

    timeString 			= ValuesNames.timestamp.name
    adcString 			= ValuesNames.adc.name
    voltageString 		= ValuesNames.voltage.name
    temperatureString 	= ValuesNames.temperature.name
    rHumidityString		= ValuesNames.rHumidity.name
    aHumidityString 	= ValuesNames.aHumidity.name
    pressureString 		= ValuesNames.pressure.name
    fanSpeedString 		= ValuesNames.fanSpeed.name
            
    def __init__(self):
        pass

    def open(self):
        pass

    def pca_set_fans_speed(self, percentage):
        pass

    def readData(self):
            return { 	
                        ValuesNames.timestamp.name		: dt.datetime.now(),  
                        ValuesNames.adc.name			: 28908,
                        ValuesNames.voltage.name		: 1.10283,
                        ValuesNames.temperature.name	: 6.2,
                        ValuesNames.rHumidity.name	    : 97.5,
                        ValuesNames.aHumidity.name      : 0.00717,
                        ValuesNames.pressure.name	    : 986.1,
                        ValuesNames.ch4.name	        : 2.2,
                        ValuesNames.fanSpeed.name	    : 0,
                    }
            
