from datetime import datetime

from matplotlib.pyplot import phase_spectrum

from measurementServer.calibration.calibrationFunctions import ch4Func1
from .enums import *
from .series import Series
from .measurement import Measurement
from .referenceData import ReferenceData
from .model import Model
from .calibration import Calibration



from dataclasses import dataclass
@dataclass
class PhysicalValue:
	name : str = ''
	description : str = ''
	units : str = ''

	def getString(self):
		if not self.units:
			return self.description
		return '{}, {}'.format(self.description, self.units)

	def getShortString(self):
		if not self.units:
			return self.description
		return '{}, {}'.format(self.name, self.units)	

@dataclass
class ValuesNames:
	timestamp 		: PhysicalValue = PhysicalValue('timestamp',	'Timestamp'							, ''		)
	adc  			: PhysicalValue = PhysicalValue('ADC',			'ADC value'							, ''		)
	voltage 		: PhysicalValue = PhysicalValue('V', 			'Voltage'							, 'volt'	)
	resistance 		: PhysicalValue = PhysicalValue('R', 			'Resistance'						, 'Ohm'		) 
	temperature 	: PhysicalValue = PhysicalValue('T', 			'Temperature'						, 'Celsius'	)
	rHumidity		: PhysicalValue = PhysicalValue('rH', 			'Relative Humidity'					, '%'		)
	aHumidity		: PhysicalValue = PhysicalValue('aH', 			'Absolute Humidity'					, 'kg*m^-3'	)
	pressure      	: PhysicalValue = PhysicalValue('P', 			'Pressure'							, 'Pascal'	)
	ch4 			: PhysicalValue = PhysicalValue('CH4', 			'Methane concentration'				, 'ppm'		)
	rsr0			: PhysicalValue = PhysicalValue('Rs/R0', 		'Relative sensor response'			, ''		)
	ch4Ref			: PhysicalValue = PhysicalValue('CH4Ref', 		'Reference Methane Concentration'	, 'ppm' 	)

__all__ = ['Series', 'Measurement', 'Model', 'Calibration', 'ReferenceData', 'MeasureType', 'Status', 'timeformat', 'ValuesNames']