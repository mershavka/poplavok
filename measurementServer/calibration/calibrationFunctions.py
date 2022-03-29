import numpy as np
from ..common import ValuesNames

def V0_pow_aH_T(X, g, m, S, h, n):
    aH = X[ValuesNames.aHumidity.name]
    T = X[ValuesNames.temperature.name]
    result = g * np.array(aH) ** h + m * np.array(T) ** n + S
    return result

def V0_pow_aH(X, g, h, S):
    aH = X[ValuesNames.aHumidity.name]
    result = g * np.array(aH) ** h + S
    return result

def V0_pow_T(X, g, h, S):
    T = X[ValuesNames.temperature.name]
    result = g * np.array(T) ** h + S
    return result

def lin_X(x, a, b):
    x_key = list(x.keys())[0]
    x = x[x_key]
    return a * np.array(x) + b

def V0_lin_aH(X, a, b):
	aH = X[ValuesNames.aHumidity.name]    
	return a * np.array(aH) + b

def V0_lin_T(X,a,b):
	T = X[ValuesNames.temperature.name]
	return a * np.array(T) + b

def V0_exp_T(X, a, b, c):
	T = X[ValuesNames.temperature.name]
	return a * np.exp(b * T) + c

def V0_exp_aH(X, a, b, c):
	aH = X[ValuesNames.aHumidity.name]
	return a * np.exp(b * aH) + c

def CH4LR_lin_CH4(X,a,b):
	CH4 = X[ValuesNames.ch4.name]
	return a * np.array(CH4) + b

def V0_lin_aH_T(X, g, m, S):
    aH = X[ValuesNames.aHumidity.name]
    T = X[ValuesNames.temperature.name]
    return g*np.array(aH) + m*np.array(T) + S

def V0_fraction_X(x, g, S):
    x_key = list(x.keys())[0]
    x = x[x_key]
    return g* np.array(x)/(S +  np.array(x))

def ch4_lin_R_rH_T(X, a, b, c, K):
    R = X[ValuesNames.rsr0.name]
    rH = X[ValuesNames.rHumidity.name]
    T = X[ValuesNames.temperature.name]
    return a*np.array(R) + b*np.array(rH) + c*np.array(T) + K

def ch4_pow_R_rH_T(X, a, b, c, d, e, f, K):
    R = X[ValuesNames.rsr0.name]
    rH = X[ValuesNames.rHumidity.name]
    T = X[ValuesNames.temperature.name]
    return a*np.array(R)**b + c*np.array(rH)**d + e*np.array(T)**f + K

def ch4_nonlin_R_rH_T(X, a, b, c, d, K):
    R = X[ValuesNames.rsr0.name]
    rH = X[ValuesNames.rHumidity.name]
    T = X[ValuesNames.temperature.name]
    return a*np.array(R)**b * (1 + c*np.array(rH) + d*np.array(T)) + K

def ch4_nonlin_R_aH_T(X, a, b, c, d, K):
    R = X[ValuesNames.rsr0.name]
    aH = X[ValuesNames.aHumidity.name]
    T = X[ValuesNames.temperature.name]
    return a*np.array(R)**b * (1 + c*np.array(aH) + d*np.array(T)) + K

def ch4_nonlin_R_aH(X, a, b, c, K):
    R = X[ValuesNames.rsr0.name]
    aH = X[ValuesNames.aHumidity.name]
    return a*np.array(R)**b * (1 + c*np.array(aH)) + K

def RsR0_calc(X):
    V0 = X[ValuesNames.voltage0.name]
    V = X[ValuesNames.voltage.name]    
    Vref = 1.024
    return (np.array(V0) - Vref) / (np.array(V) - Vref)

calib1Functions = {
    'linFunc_aH'	: (V0_lin_aH,  [ValuesNames.aHumidity.name], [ValuesNames.voltage0.name]),
    'linFunc_T'	    : (V0_lin_T,  [ValuesNames.temperature.name], [ValuesNames.voltage0.name]),
    'powFunc_aH'   	: (V0_pow_aH,  [ValuesNames.aHumidity.name], [ValuesNames.voltage0.name]),
    'powFunc_T'   	: (V0_pow_T,  [ValuesNames.temperature.name], [ValuesNames.voltage0.name]),
	'expFunc_aH'   	: (V0_exp_aH,  [ValuesNames.aHumidity.name], [ValuesNames.voltage0.name]),
    'expFunc_T'   	: (V0_exp_T,  [ValuesNames.temperature.name], [ValuesNames.voltage0.name]),
    'powSurf_aHT'   : (V0_pow_aH_T,  [ValuesNames.aHumidity.name, ValuesNames.temperature.name], [ValuesNames.voltage0.name]),
    'plane_aHT'		: (V0_lin_aH_T,   [ValuesNames.aHumidity.name,ValuesNames.temperature.name], [ValuesNames.voltage0.name]),
    'hyperbola_aH'	: (V0_fraction_X,   [ValuesNames.aHumidity.name], [ValuesNames.voltage0.name]),
    'hyperbola_T'	: (V0_fraction_X,   [ValuesNames.temperature.name], [ValuesNames.voltage0.name]),
}

calib2Functions = {
    'ch4Func1_rHT' : (ch4_lin_R_rH_T, [ValuesNames.rsr0.name, ValuesNames.rHumidity.name, ValuesNames.temperature.name], [ValuesNames.ch4.name]),
    'ch4Func2_rHT' : (ch4_pow_R_rH_T, [ValuesNames.rsr0.name, ValuesNames.rHumidity.name, ValuesNames.temperature.name], [ValuesNames.ch4.name]),
    'ch4Func3_rHT' : (ch4_nonlin_R_rH_T, [ValuesNames.rsr0.name, ValuesNames.rHumidity.name, ValuesNames.temperature.name], [ValuesNames.ch4.name]),
    'ch4Func4_aHT' : (ch4_nonlin_R_aH_T, [ValuesNames.rsr0.name, ValuesNames.aHumidity.name, ValuesNames.temperature.name], [ValuesNames.ch4.name]),
    'ch4Func8_aH'  : (ch4_nonlin_R_aH, [ValuesNames.rsr0.name, ValuesNames.aHumidity.name], [ValuesNames.ch4.name])
}

calib3Functions = {
    'lin_func_CH4pred' : (CH4LR_lin_CH4, [ValuesNames.ch4.name], [ValuesNames.ch4LR.name])
}

def functionByName(function_name):
	if function_name in calib1Functions:
		return calib1Functions[function_name][0]
	elif function_name in calib2Functions:
		return calib2Functions[function_name][0]
	elif function_name in calib3Functions:
		return calib3Functions[function_name][0]
	return None