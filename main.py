# from measurementServer.client import PyroMeasurementClient
# from measurementServer.common import *
from measurementServer.server import MeasurementServer
from datetime import datetime

# datetime.fromisoformat()

timestrings = [
    '2021-11-22 13:30:03.258601',
	'2021-11-22 13:30:05.259419',
	'2021-11-22 13:30:06.259882',
	'2021-11-22 13:30:07.259971',
	'2021-11-22 13:30:08.260496',
	'2021-11-22 13:30:09.260864',
	'2021-11-22 13:30:10.260983',
	'2021-11-22 13:30:12.261718'
]
timestamps = [datetime.fromisoformat(s) for s in timestrings]

ch4Ref = [
    5.1,
    5.2,
    4.9,
    5.2,
    5,
    5,
    5.1,
    5
]

ms = MeasurementServer()
# ms.createSeries("Test with dataframe")
# ms.runMeasurement(10, 1, 'With df')
# print(ms.getSeriesList())
# ms.uploadReferenceData(2, timestamps, ch4Ref)
ms.startCalibration("Test",1,2)
# ms.ma.generateTestDatasets(step=2)

# pmc = PyroMeasurementClient()
# print(pmc.getServerStatus())
# print(pmc.getSeriesList())
# pmc.runMeasurement(10, 1, 'TTTT')
# pmc.createSeries('With sensor',MeasureType.COMMON)
# print(pmc.getSeriesList())
