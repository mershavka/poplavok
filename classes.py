from math import sqrt
from scipy.optimize import curve_fit
import numpy as np

class Model_fitting:

	def __init__(self, predictors, dependent_variable, dependence_function, variable_name = 'undefined'):
		 self.variable_name = variable_name
		 self.X = predictors
		 self.y = dependent_variable
		 self.function = dependence_function
		 self.__fit()

	def display_info(self):
		print('Это модель для параметра "{}"'.format(self.variable_name))

	def __fit(self):
		popt, pcov = curve_fit(self.function, self.X, self.y)
		self.predictors_count = np.size(self.X, 0)
		self.y_hat = self.function(self.X, *popt)
		self.ss_residual = sum((self.y-self.y_hat)**2)
		self.ss_total = sum((self.y-np.mean(self.y))**2)     
		self.r_squared = 1 - (float(self.ss_residual))/self.ss_total
		self.adjusted_r_squared = 1 - (1-self.r_squared)*(len(self.y)-1)/(len(self.y)-self.predictors_count)
		self.rmse = sqrt(self.ss_residual / len(self.y))
	
#Residual sum of squares (сумма квадратов остатков)
	def ss_residual(self):
		return self.ss_residual
#Total sum of squares (общая сумма квадратов)
	def ss_total(self):
		return self.ss_total
#Скорректированный коэффициент детерминации (adjusted)
	def adjusted_r_squared(self):
		return self.adjusted_r_squared
#Коэффициент детерминации — R-квадрат
	def r_squared(self):
		return self.r_squared
#Root Mean Square Error Среднеквадратическая ошибка модели
	def rmse(self):
		return self.rmse
#Количество предикторов (независимых переменных)
	def predictors_count(self):
		return self.predictors_count
