from .enums import *
from .series import Series
from .measurement import Measurement
from .referenceData import ReferenceData
from .model import Model
from .calibration import Calibration

from dataclasses import dataclass
@dataclass
class ValuesNames:
    timeString          : str = 'Time'
    adcString           : str = 'ADC value'
    voltageString       : str = 'Voltage, V'
    resistanceString    : str = 'Resistance, Om'
    temperatureString   : str = 'Temperature, C'
    rHumidityString     : str = 'Related Humidity, %'
    aHumidityString     : str = 'Absolute Humidity, kg/m^3'
    pressureString      : str = 'Pressure, hPa'
    ch4String           : str = 'CH4, ppm'

__all__ = ['Series', 'Measurement', 'Model', 'Calibration', 'ReferenceData', 'MeasureType', 'Status', 'timeformat']