# from typing import final
import pandas
import numpy as np
from models import ModelFirst, ModelSecond
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



#дублируется в файле experiment
def appendRowToCsv(filename, listOfElements):
    with open(filename, 'a+', newline ='') as writeObj:
        writer = csv.writer(writeObj)
        writer.writerow(listOfElements)

class CalibrationModule:

    relativeHumidity = "rH"
    absoluteHumidity = "aH"
    temperature      = "T"

    calib1Models = {
        'powFunc_aHT'   : ModelFirst(pow_func,  ["aH","T"]),
        'linFunc_aH'	: ModelFirst(lin_func,  ["aH"]),
        'linFunc_T'	    : ModelFirst(lin_func,  ["T"]),
        'V2Func_aHT'	: ModelFirst(V2_func,   ["aH","T"]),
        'V5Func_aH'	    : ModelFirst(V5_func,   ["aH"]),
        'V5Func_T'	    : ModelFirst(V5_func,   ["T"]),
    }

    calib2Models = {
        'ch4Func1_rHT' : ModelSecond(ch4Func1, ["R","rH","T"]),
        'ch4Func2_rHT' : ModelSecond(ch4Func2, ["R","rH","T"]),
        'ch4Func3_rHT' : ModelSecond(ch4Func3, ["R","rH","T"]),
        'ch4Func4_rHT' : ModelSecond(ch4Func4, ["R","aH","T"]),
        'ch4Func8_rHT' : ModelSecond(ch4Func8, ["R","aH"])
    }

    def concatCsv(dirPath):
        all_files = glob.glob(dirPath + "/*.csv")
        li = []
        for filename in all_files:
            df = pandas.read_csv(filename, delimiter=',')
            li.append(df)
        frame = pandas.concat(li, axis=0, ignore_index=True)
        return frame

    def __init__(self):
        self.csvHeader = ['Time', 'ADC', 'V', 'R', 'T', 'rH', 'aH', 'P']
    
    def calibrateFirstStep(dirPath, resultPath):
        df = CalibrationModule.concatCsv(dirPath)
        firstModels = CalibrationModule.calib1Models.values()
        appendRowToCsv(file_name, ['CalibrationDataDirectory','FunctionName','PredictorNames', 'R2Adjusted', 'RMSE','OptimalModelParametres'])
        for model in firstModels:
            X = []
            for predictor in model.predictor_names:
                X.append(df[predictor].tolist())
            model.fit(tuple(X),  df['V'].tolist())           
            print(tuple(model.popt))
            appendRowToCsv(resultPath, [dirPath, model.function.__name__, model.predictor_names, model.adjusted_r_squared, model.rmse, model.popt])	

    def calibrateSecondStep():
        pass

fileNames = ['exp_2021_06_23_185934.csv']

x_data_humidity = []
x_data_temperature = []
y_data_v = []



oneArgumentFunctions = [lin_func, funcV5]
twoArgumentFunctions = [funcV2, pow_func]
threeArgumentFunctions = []

#step1
try:
    modelsFrame = pandas.DataFrame()
    for name in fileNames:
        df = pandas.read_csv(name, delimiter= ',')
        df.set_axis(['Time', 'ADC', 'V', 'R', 'T', 'RH', 'P'], axis = 'columns', inplace = True)
        x_data_humidity = x_data_humidity + df['RH'].tolist()
        x_data_temperature = x_data_temperature + df['T'].tolist()
        y_data_v = y_data_v + df['V'].tolist()

    # plt.plot(x_data_humidity, y_data_v, 'b', label='data') #% - форматирование строк в стиле printf
    # plt.xlabel('humidity')
    # plt.ylabel('voltage')
    file_name = ('calibration_1step_{:%Y_%m_%d_%H%M%S}.csv').format(dt.datetime.now())
    appendRowToCsv(file_name, ['FunctionName','NumberOfParametres', 'R2Adjusted', 'RMSE','popt'])

    X = x_data_humidity, x_data_temperature
    
    for f1 in oneArgumentFunctions:
        for x in X:
            my_class = Model_fitting(f1, x, y_data_v)
            print(tuple(my_class.popt))
            appendRowToCsv(file_name, [f1.__name__, 1, my_class.adjusted_r_squared, my_class.rmse, my_class.popt])

    for f2 in twoArgumentFunctions:
        my_class = Model_fitting(f2, X, y_data_v)
        print(tuple(my_class.popt))
        appendRowToCsv(file_name, [f2.__name__, 2, my_class.adjusted_r_squared, my_class.rmse, my_class.popt])

    # plt.show()


finally:
    print("")



#step2
dataFilePathes = []
cal1FilePath = []
try:
    x_data_humidity = []
    x_data_temperature = []
    y_data_v = []

    for name in dataFilePathes:
        df = pandas.read_csv(name, delimiter= ',')
        df.set_axis(['Time', 'ADC', 'V', 'R', 'T', 'RH', 'P'], axis = 'columns', inplace = True)
        x_data_humidity = x_data_humidity + df['RH'].tolist()
        x_data_temperature = x_data_temperature + df['T'].tolist()
        y_data_v = y_data_v + df['V'].tolist()

    model = pandas.read_csv(cal1FilePath, delimiter= ',')
    df.set_axis(['FunctionName','NumberOfParametres', 'variables', 'R2Adjusted', 'RMSE','popt'], axis = 'columns', inplace = True)
    functionName = model.loc[[0], "FunctionName"]
    modelPopt = model.loc[[0], "popt"]

    v0_data = eval(functionName + "()")
    R_data = Rs_by_R0_from_V0(v0_data, y_data_v, 1.024)

    file_name = ('calibration_2step_{:%Y_%m_%d_%H%M%S}.csv').format(dt.datetime.now())
    appendRowToCsv(file_name, ['FunctionName','NumberOfParametres', 'variables', 'R2Adjusted', 'RMSE','popt'])

    X = x_data_humidity, x_data_temperature
    
    for f1 in threeArgumentFunctions:
        for x in X:
            my_class = Model_fitting(f1, x, y_data_v)
            print(tuple(my_class.popt))
            appendRowToCsv(file_name, [f1.__name__, 1, my_class.adjusted_r_squared, my_class.rmse, my_class.popt])

    for f2 in twoArgumentFunctions:
        my_class = Model_fitting(f2, X, y_data_v)
        print(tuple(my_class.popt))
        appendRowToCsv(file_name, [f2.__name__, 2, my_class.adjusted_r_squared, my_class.rmse, my_class.popt])

    # plt.show()


finally:
    print("")