import csv
import pandas
import matplotlib.pyplot as plt

df = pandas.read_csv('Calibration_Step_Two.csv', delimiter= ';')
df.set_axis(['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'T', 'RH', 'Vl', 'CH4'], axis = 'columns', inplace = True)

def Rs_by_R0_from_V0(func, ):
