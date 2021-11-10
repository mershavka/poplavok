import numpy as np
from ..common import ValuesNames

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

calib1Functions = {
    'powFunc_aHT'   : (pow_func,  [ValuesNames.aHumidity.name, ValuesNames.temperature.name]),
    'linFunc_aH'	: (lin_func,  [ValuesNames.aHumidity.name]),
    'linFunc_T'	    : (lin_func,  [ValuesNames.temperature.name]),
    'V2Func_aHT'	: (V2_func,   [ValuesNames.aHumidity.name,ValuesNames.temperature.name]),
    'V5Func_aH'	    : (V5_func,   [ValuesNames.aHumidity.name]),
    'V5Func_T'	    : (V5_func,   [ValuesNames.temperature.name]),
}

calib2Functions = {
    'ch4Func1_rHT' : (ch4Func1, [ValuesNames.rsr0.name, ValuesNames.rHumidity.name, ValuesNames.temperature.name]),
    'ch4Func2_rHT' : (ch4Func2, [ValuesNames.rsr0.name, ValuesNames.rHumidity.name, ValuesNames.temperature.name]),
    'ch4Func3_rHT' : (ch4Func3, [ValuesNames.rsr0.name, ValuesNames.rHumidity.name, ValuesNames.temperature.name]),
    'ch4Func4_aHT' : (ch4Func4, [ValuesNames.rsr0.name, ValuesNames.aHumidity.name, ValuesNames.temperature.name]),
    'ch4Func8_aH'  : (ch4Func8, [ValuesNames.rsr0.name, ValuesNames.aHumidity.name])
}

calib3Functions = {
    'lin_func_CH4pred' : (lin_func, [ValuesNames.ch4.name])
}