import csv
import pandas
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
 
# with open('TGS2611_TGS2600_Calibration.csv', encoding='utf-8') as File:
#     reader = csv.reader(File, delimiter = ";")
#     count = 0
#     for row in reader:
#         if count == 0:
#             print('Файл содержит столбцы\n{:}'.format(', '.join(row)))
#             columns_names = row
#         else:
#             print(row)
#         count += 1
# print(columns_names)

df = pandas.read_csv('TGS2611_TGS2600_Calibration.csv', delimiter= ';')
df.set_axis(['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'TGS2611', 'TGS2600', 'R0', 'T', 'RH', 'Vcc', 'CH4'], axis = 'columns', inplace = True)

def exp_func(x, a, b, c):
	return a * np.exp(-b * x) + c

def lin_func(x, a, b):
	return a * np.array(x) + b

def lin_func_2(x1, x2, a, b, c):
	return a * np.array(x1) + b * np.array(x2) + c

def power_func(x1, x2, a, b, c, h, n ):
	return a * np.power(x1, h) + b * np.power(x2, n) + c

x_data_humidity = df['RH'].tolist()
x_data_temperature = df['T'].tolist()
y_data_v = df['Vcc'].tolist()
plt.plot(x_data_humidity, y_data_v, 'o', linestyle = 'None', label='data')
plt.xlabel('Humidity')
plt.ylabel('V')
res = stats.linregress(x_data_humidity, y_data_v)
print([res.slope,  res.intercept])
print(f"R-squared: {res.rvalue**2:.6f}")
plt.plot(x_data_humidity, lin_func(x_data_humidity, res.slope,  res.intercept), 'r', label='fitted line')

popt, pcov = curve_fit(lin_func, x_data_humidity, y_data_v)
print(tuple(popt))
plt.plot(x_data_humidity, lin_func(x_data_humidity, *popt), 'r-', label= 'fit: a = {:.5f}, b = {:.5f}'.format(tuple(popt)[0], tuple(popt)[1]))
plt.legend()
plt.show()