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
	timestamp 		: PhysicalValue = PhysicalValue('timestamp',	'Timestamp'							, ''			)
	adc  			: PhysicalValue = PhysicalValue('ADC',			'ADC value'							, ''			)
	voltage 		: PhysicalValue = PhysicalValue('V', 			'Voltage'							, 'volt'		)
	voltage0 		: PhysicalValue = PhysicalValue('V0', 			'Background Voltage'				, 'volt'		)
	resistance 		: PhysicalValue = PhysicalValue('R', 			'Resistance'						, 'Ohm'			) 
	temperature 	: PhysicalValue = PhysicalValue('T', 			'Temperature'						, 'Celsius'		)
	rHumidity		: PhysicalValue = PhysicalValue('rH', 			'Relative Humidity'					, '%'			)
	aHumidity		: PhysicalValue = PhysicalValue('aH', 			'Absolute Humidity'					, 'kg*m^-3'		)
	pressure      	: PhysicalValue = PhysicalValue('P', 			'Pressure'							, 'hectopascal'	)
	ch4 			: PhysicalValue = PhysicalValue('CH4', 			'Methane concentration'				, 'ppm'			)
	ch4LR 			: PhysicalValue = PhysicalValue('CH4LR',		'Methane concentration LR'			, 'ppm'			)
	rsr0			: PhysicalValue = PhysicalValue('Rs/R0', 		'Relative sensor response'			, ''			)
	ch4Ref			: PhysicalValue = PhysicalValue('CH4Ref', 		'Reference Methane Concentration'	, 'ppm' 		)
	fanSpeed		: PhysicalValue = PhysicalValue('fanSpeed', 	'Fan speed'							, '%' 			)

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
		ch4LR.getString() 			: ch4LR.name,
		rsr0.getString() 			: rsr0.name,
		ch4Ref.getString() 			: ch4Ref.name,
		fanSpeed.getString() 		: fanSpeed.name,
	}

@dataclass
class ModelNames:
	model1: str = "V0Model"
	model2: str = "CH4Model"
	model3: str = "CH4LRModel"

@dataclass
class ModelParameters:
	function_name 		:str = 'function_name'     
	predictor_names 	:str = 'predictor_names'
	predictors_count    :str = 'predictors_count'
	dependent_name		:str = 'dependent_name'    
	coefficients 		:str = 'coefficients'             
	adjusted_r_squared 	:str = 'adjusted_r_squared'
	rmse 				:str = 'rmse'              
