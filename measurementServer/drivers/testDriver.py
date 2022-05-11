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
                        ValuesNames.adc.name			: 28545,
                        ValuesNames.voltage.name		: 1.09,
                        ValuesNames.temperature.name	: 23.2,
                        ValuesNames.rHumidity.name	    : 18.9,
                        ValuesNames.aHumidity.name      : 0.004,
                        ValuesNames.pressure.name	    : 971.4,
                        ValuesNames.ch4.name	        : 2.4,
                        ValuesNames.fanSpeed.name	    : 0,
                    }
            
