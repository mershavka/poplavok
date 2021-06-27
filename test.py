import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import classes

def exp_func(x, a, b,c):
	return a * np.exp(-b * x) + c

def func(X, a, b, c):
    x,y = X
    return np.log(a) + b*np.log(x) + c*np.log(y)

xdata = np.linspace(0, 4, 50)
print(np.size(xdata, 0))
y = exp_func(xdata, 2.5, 1.3, 0.5)
np.random.seed(1729)
y_noise = 0.2 * np.random.normal(size=xdata.size)
ydata = y + y_noise
plt.plot(xdata, ydata, 'b-', label='data')

popt, pcov = curve_fit(exp_func, xdata, ydata)
y_hat = exp_func(xdata, *popt)
# Звёздочка означает распаковку позиционных аргументов
legendStr = "a = {:2f}, b = {}, c = {}".format(*popt)
plt.plot(xdata, y_hat, 'r-', label=legendStr) #% - форматирование строк в стиле printf
plt.xlabel('x')
plt.ylabel('y')
plt.legend()

test = classes.Model_fitting(exp_func, xdata, ydata)
perr = np.sqrt(np.diag(test.pcov))
print("perr:", perr)
print(test.ss_residual, test.ss_total, test.r_squared, test.adjusted_r_squared)

x = np.linspace(0.1,1.1,101)
y = np.linspace(1.,2., 101)
a, b, c = 10., 4., 6.
z = func((x,y), a, b, c) * 1 + np.random.random(101) / 100
X = x,y
p0 = 8., 2., 7.# initial guesses for a,b,c:

test2 = classes.Model_fitting(func, X , z)
# print("popt2: {}, pcov2: {}".format(test2.popt, test2.pcov))

plt.show()