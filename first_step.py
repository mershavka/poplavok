import csv
import pandas
import matplotlib.pyplot as plt
import numpy as np
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
print(df['TGS2611'].tolist())

def exp_func(x, a, b,c):
	return a * np.exp(-b * x) + c

def lin_func(x, a, b):
	return a * np.array(x) + b

x_data_humidity = df['R0'].tolist()
y_data_v = df['Vcc'].tolist()
plt.plot(x_data_humidity, y_data_v, 'b-', label='data')
plt.show()
# popt, pcov = curve_fit(lin_func, x_data_humidity, y_data_v)
# print(popt)
# plt.plot(x_data_humidity, lin_func(x_data_humidity, *popt), 'r-', label='fit: a=%5.3f, b=%5.3f' % tuple(popt))
# plt.xlabel('Humidity')
# plt.ylabel('V')
# plt.legend()
# plt.show()