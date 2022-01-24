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
            
    def __init__(self):
        pass

    def open(self):
        pass

    def readData(self):
            return { 	
                        ValuesNames.timestamp.name		: dt.datetime.now(),  
                        ValuesNames.adc.name			: 52428,
                        ValuesNames.voltage.name		: 2,
                        ValuesNames.temperature.name	: 25,
                        ValuesNames.rHumidity.name	    : 60,
                        ValuesNames.aHumidity.name      : 0.014,
                        ValuesNames.pressure.name	    : 1013.25,
                    }
            
