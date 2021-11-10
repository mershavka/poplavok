from ..common import *
from ..calibration import calibrationModel
import pandas

class methaneAnalyzer:
	
	def __init__(self):
		self.modelTemplates = []
		

	def passDataToCalibrationModule(self, series1Path, series2Path):
		models = self.calibrationModelsPreparing()
		series1Data = self
