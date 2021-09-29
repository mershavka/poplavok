from math import sqrt
from numpy.core.fromnumeric import nonzero
from scipy.optimize import curve_fit
import numpy as np

class ModelFirst:

    def __init__(self, dependence_function, predictor_names):
        self.function = dependence_function
        self.predictor_names = predictor_names
        self.popt = None
    
    def fit(self, predictors, dependent_variable):
        self.X = predictors
        self.y = dependent_variable
        self.__fit()

    def calculate(self, X):
        if self.popt == None:
            return None
        return self.function(X, *self.popt)

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


class ModelSecond:
    def __init__(self, dependence_function, predictor_names):
        self.function = dependence_function
        self.predictor_names = predictor_names
        self.popt = None
        self.modelV0 = None

    def lin_func(self, ch4, k, M):
        return k * np.array(ch4) + M

    def fit(self, predictors, ch4_reference):
        self.X = predictors
        self.ch4_observed = np.array(ch4_reference)
        self.__fit()
    
    def calculate(self, X1, X2 ):        
        V0 = self.modelV0.calculate(X1, self.modelV0.popt)

    def __fit(self):
        self.popt, self.pcov = curve_fit(self.function, self.X, self.y)
        #Количество предикторов (независимых переменных)
        self.predictors_count = np.ndim(self.X)
        self.ch4_predicted = self.function(self.X, *self.popt)
        self.modelLinCH4 = ModelFirst(ModelSecond.lin_func, "Calculated CH4")
        self.modelLinCH4.fit( self.ch4_predicted, self.ch4_observed)
        self.k = self.modelLinCH4.popt[0]
        self.M = self.modelLinCH4.popt[1]
        self.adjusted_r_squared = self.modelLinCH4.adjusted_r_squared
        self.rmse = self.modelLinCH4.rmse

        
        