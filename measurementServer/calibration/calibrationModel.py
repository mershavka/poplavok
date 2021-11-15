from math import sqrt
from numpy.core.fromnumeric import nonzero
from scipy.optimize import curve_fit
import numpy as np

class CalibrationModelTemplate:
    def __init__(self, dependence_function, predictor_names, dependent_name):
        self.function = dependence_function
        self.predictor_names = predictor_names
        self.dependent_name = dependent_name


class CalibrationModel:

    def __init__(self, dependence_function, predictor_names, dependent_name):
        self.function = dependence_function
        self.predictor_names = predictor_names
        self.dependent_name = dependent_name
        self.coefs = None
    
    def fit(self, predictors, dependent_variable):
        self.X = predictors
        self.y = dependent_variable
        self.__fit()

    def calculate(self, X):
        if self.coefs == None:
            return None
        return self.function(X, *self.coefs)

    def __fit(self):
        self.coefs, self.pcov = curve_fit(self.function, self.X, self.y)
        #Количество предикторов (независимых переменных)
        self.predictors_count = np.ndim(self.X)
        self.y_hat = self.function(self.X, *self.coefs)
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

        
        