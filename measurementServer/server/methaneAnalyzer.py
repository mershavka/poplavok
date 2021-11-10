from measurementServer.calibration import calibrationModel
from measurementServer.calibration.calibrationFunctions import lin_func
from ..common import *
from ..calibration import *
import pandas

class methaneAnalyzer:
	
	def __init__(self):
		self.modelTemplates = [calibrationModel(lin_func, ), calibrationModel()]


	def passDataToCalibrationModule(self, series1Path, series2Path):
		models = self.calibrationModelsPreparing()
		series1Data = self
