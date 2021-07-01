# from typing import final
import pandas
import numpy as np
from classes import Model_fitting
import matplotlib.pyplot as plt
import datetime as dt
import csv

fileNames = ['exp_2021_06_23_185934.csv']

x_data_humidity = []
x_data_temperature = []
y_data_v = []

#дублируется в файле experiment
def appendRowToCsv(filename, listOfElements):
	with open(filename, 'a+', newline ='') as writeObj:
		writer = csv.writer(writeObj)
		writer.writerow(listOfElements)

def pow_func(X, g, m, S, h, n):
	H,T = X
	return g * np.array(H)^h +m * np.array(T)^n + S

def lin_func(x, a, b):
	return a * np.array(x) + b

def funcV2(X, g, m, S):
	H,T = X
	return g*np.array(H) + m*np.array(T) + S

def funcV5(x, g, S):
	return g* np.array(x)/(S +  np.array(x))

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

def Rs_by_R0_from_V0(V0, VL, Vref):
	return (np.array(V0) - Vref) / (np.array(VL) - Vref)

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