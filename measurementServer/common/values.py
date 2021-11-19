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
	voltage0 		: PhysicalValue = PhysicalValue('V0', 			'Background Voltage'				, 'volt'	)
	resistance 		: PhysicalValue = PhysicalValue('R', 			'Resistance'						, 'Ohm'		) 
	temperature 	: PhysicalValue = PhysicalValue('T', 			'Temperature'						, 'Celsius'	)
	rHumidity		: PhysicalValue = PhysicalValue('rH', 			'Relative Humidity'					, '%'		)
	aHumidity		: PhysicalValue = PhysicalValue('aH', 			'Absolute Humidity'					, 'kg*m^-3'	)
	pressure      	: PhysicalValue = PhysicalValue('P', 			'Pressure'							, 'Pascal'	)
	ch4 			: PhysicalValue = PhysicalValue('CH4', 			'Methane concentration'				, 'ppm'		)
	rsr0			: PhysicalValue = PhysicalValue('Rs/R0', 		'Relative sensor response'			, ''		)
	ch4Ref			: PhysicalValue = PhysicalValue('CH4Ref', 		'Reference Methane Concentration'	, 'ppm' 	)

	stringToName = {
		timestamp.getString() 		: timestamp.name,
		adc.getString() 			: adc.name,
		voltage.getString() 		: voltage.name,
		voltage0.getString() 		: voltage0.name,
		resistance.getString() 		: resistance.name,	
		temperature.getString() 	: temperature.name, 
		rHumidity.getString() 		: rHumidity.name,
		aHumidity.getString() 		: aHumidity.name,
		pressure.getString() 		: pressure.name, 
		ch4.getString() 			: ch4.name,
		rsr0.getString() 			: rsr0.name,
		ch4Ref.getString() 			: ch4Ref.name,
	}
