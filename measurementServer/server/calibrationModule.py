# from typing import final
from .models import ModelFirst, ModelSecond

import pandas
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import csv
import glob

def pow_func(X, g, m, S, h, n):
    H,T = X
    return g * np.array(H)^h +m * np.array(T)^n + S

def lin_func(x, a, b):
    return a * np.array(x) + b

def V2_func(X, g, m, S):
    H,T = X
    return g*np.array(H) + m*np.array(T) + S

def V5_func(x, g, S):
    return g* np.array(x)/(S +  np.array(x))

def ch4Func1(X, a, b, c, K):
    R, rH, T = X
    return a*np.array(R) + b*np.array(rH) + c*np.array(T) + K

def ch4Func2(X, a, b, c, d, e, f, K):
    R, rH, T = X
    return a*np.array(R)^b + c*np.array(rH)^d + e*np.array(T)^f + K

def ch4Func3(X, a, b, c, d, K):
    R, rH, T = X
    return a*np.array(R)^b * (1 + c*np.array(rH) + d*np.array(T)) + K

def ch4Func4(X, a, b, c, d, K):
    R, aH, T = X
    return a*np.array(R)^b * (1 + c*np.array(aH) + d*np.array(T)) + K

def ch4Func8(X, a, b, c, K):
    R, aH = X
    return a*np.array(R)^b * (1 + c*np.array(aH)) + K

def stringToFloatList(s):
    s = s.strip('][').split(' ')
    while '' in s:    
        s.remove('')
    return [float(i) for i in s]

#дублируется в файле experiment
def appendRowToCsv(filename, listOfElements):
    with open(filename, 'a+', newline ='') as writeObj:
        writer = csv.writer(writeObj)
        writer.writerow(listOfElements)

class CalibrationModule:

    relativeHumidity = "rH"
    absoluteHumidity = "aH"
    temperature      = "T"

    def __init__(self):
        self.csvHeader = ['Time', 'ADC', 'V', 'R', 'T', 'rH', 'aH', 'P']
        self.modelV0Header = ['CalibrationDataDirectory','FunctionName','PredictorNames', 'R2Adjusted', 'RMSE','OptimalModelParametres']
        self.modelCH4Header = ['CalibrationDataDirectory', 'FirstStepCalibrationPath','FunctionName','PredictorNames', 'R2Adjusted', 'RMSE','OptimalModelParametres', 'Slope k' , 'Intercept M']

    calib1Models = {
        'powFunc_aHT'   : (pow_func,  ["aH","T"]),
        'linFunc_aH'	: (lin_func,  ["aH"]),
        'linFunc_T'	    : (lin_func,  ["T"]),
        'V2Func_aHT'	: (V2_func,   ["aH","T"]),
        'V5Func_aH'	    : (V5_func,   ["aH"]),
        'V5Func_T'	    : (V5_func,   ["T"]),
    }

    calib2Models = {
        'ch4Func1_rHT' : (ch4Func1, ["Rs/R0","rH","T"]),
        'ch4Func2_rHT' : (ch4Func2, ["Rs/R0","rH","T"]),
        'ch4Func3_rHT' : (ch4Func3, ["Rs/R0","rH","T"]),
        'ch4Func4_aHT' : (ch4Func4, ["Rs/R0","aH","T"]),
        'ch4Func8_aH'  : (ch4Func8, ["Rs/R0","aH"])
    }

    def loadModelV0FromFile(self, cal1Path):
        df = pandas.read_csv(cal1Path, delimiter=',')
        df.set_axis(self.modelV0Header, axis = 'columns', inplace = True)
        funcName = df['FunctionName'][0]
        popt = stringToFloatList(df['OptimalModelParametres'][0])
        model = ModelFirst(*CalibrationModule.calib1Models[funcName])
        model.popt = popt
        return model


    def loadModelCH4FromFile(self, cal2Path):
        df = pandas.read_csv(cal2Path, delimiter=',')
        df.set_axis(self.modelCH4Header, axis = 'columns', inplace = True)
        k = df['Slope k'][0]
        M = df['Intercept M'][0]
        cal1Path = df['FirstStepCalibrationPath'][0]
        funcName = df['FunctionName'][0]
        popt = stringToFloatList(df['OptimalModelParametres'][0])
        model = ModelSecond(*CalibrationModule.calib2Models[funcName])
        model.popt = popt
        model.k = k
        model.M = M
        model.modelV0 = CalibrationModule.loadModelV0FromFile(cal1Path)
        return model

    def bestV0Model():
        pass

    def bestCH4Model():
        pass

    def concatCsv(dirPath):
        all_files = glob.glob(dirPath + "/*.csv")
        li = []
        for filename in all_files:
            df = pandas.read_csv(filename, delimiter=',')
            li.append(df)
        frame = pandas.concat(li, axis=0, ignore_index=True)
        return frame

    def Rs_by_R0_from_V0(V0, VL, Vref):
	    return (np.array(V0) - Vref) / (np.array(VL) - Vref)

    
    def calibrateFirstStep(self, dirPath, resultPath):
        df = CalibrationModule.concatCsv(dirPath)
        df.set_axis(self.csvHeader, axis = 'columns', inplace = True)
        appendRowToCsv(resultPath, self.modelV0Header)
        for modelName, modelParams in CalibrationModule.calib1Models.items():
            X = []
            model = ModelFirst(*modelParams)
            for predictor in model.predictor_names:
                X.append(df[predictor].tolist())
            model.fit(tuple(X),  df['V'].tolist())           
            print(tuple(model.popt))
            appendRowToCsv(resultPath, [dirPath, modelName, model.predictor_names, model.adjusted_r_squared, model.rmse, model.popt])
        return 

    def calibrateSecondStep(self, dirPath, cal1Path, referenceDirPath, resultPath):
        df = CalibrationModule.concatCsv(dirPath)
        df.set_axis(self.csvHeader, axis = 'columns', inplace = True)
        appendRowToCsv(resultPath, self.modelCH4Header)
        ch4df =  CalibrationModule.concatCsv(referenceDirPath)
        ch4df.set_axis(['Time', 'CH4'], axis = 'columns', inplace = True)
        V0Model = CalibrationModule.loadModelV0FromFile(cal1Path)
        X = []
        for predictor in V0Model.predictor_names:
            X.append(df[predictor].tolist())
        V0 = V0Model.calculate(X)
        RsR0 = CalibrationModule.Rs_by_R0_from_V0(V0, df['V'].tolist(), 1.024)
        for modelName, modelParams in CalibrationModule.calib2Models.items():
            X = [RsR0]
            model = ModelSecond(*modelParams)
            model.modelV0 = V0Model
            for predictor in model.predictor_names:
                if predictor != "Rs/R0":
                    X.append(df[predictor].tolist())
            model.fit(tuple(X),  ch4df['CH4'].tolist())         
            print(tuple(model.popt))
            appendRowToCsv(resultPath, [dirPath, cal1Path, modelName, model.predictor_names, model.adjusted_r_squared, model.rmse, model.popt, model.k, model.M])
        return	