from measurementServer.pyro4iface import PyroMeasurementClient
from measurementServer.common import *

pmc = PyroMeasurementClient()
print(pmc.getServerStatus())
pmc.createSeries('1',MeasureType.COMMON)
print(pmc.getSeriesList())
