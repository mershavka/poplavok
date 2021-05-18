from math import sqrt
from scipy.optimize import curve_fit
import numpy as np

class Model_fitting:

	def __init__(self,  dependence_function, predictors, dependent_variable, variable_name = 'undefined'):
		 self.variable_name = variable_name
		 self.X = predictors
		 self.y = dependent_variable
		 self.function = dependence_function
		 self.__fit()

	def display_info(self):
		print('Это модель для параметра "{}"'.format(self.variable_name))

	def __fit(self):

		self.popt, self.pcov = curve_fit(self.function, self.X, self.y)
		#Количество предикторов (независимых переменных)
		self.predictors_count = np.ndim(self.X)
		self.y_hat = self.function(self.X, *self.popt)
		#Residual sum of squares (сумма квадратов остатков)
		self.ss_residual = sum((self.y-self.y_hat)**2)
		 #Total sum of squares (общая сумма квадратов)
		self.ss_total = sum((self.y-np.mean(self.y))**2)
		#Коэффициент детерминации — R-квадрат  
		self.r_squared = 1 - (float(self.ss_residual))/self.ss_total
		#Скорректированный коэффициент детерминации (adjusted)
		self.adjusted_r_squared = 1 - (1-self.r_squared)*(len(self.y)-1)/(len(self.y)-self.predictors_count)
		#Root Mean Square Error Среднеквадратическая ошибка модели
		self.rmse = sqrt(self.ss_residual / len(self.y))
	
