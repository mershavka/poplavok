from measurementServer.client import PyroMeasurementClient
from measurementServer.common import *

pmc = PyroMeasurementClient()
print(pmc.getServerStatus())
print(pmc.getLastData())
# pmc.runMeasurement(10, 1, 'TTTT')
# pmc.createSeries('With sensor',MeasureType.COMMON)
# print(pmc.getSeriesList())
