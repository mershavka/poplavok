# from measurementServer.client import PyroMeasurementClient
# from measurementServer.common import *
from measurementServer.server import MeasurementServer
from datetime import datetime

# datetime.fromisoformat()

timestrings = [
    '2021-11-21 19:02:23.036310',
    '2021-11-21 19:02:24.036316',
    '2021-11-21 19:02:25.036319',
    '2021-11-21 19:02:27.036331',
    '2021-11-21 19:02:28.036329',
    '2021-11-21 19:02:29.036347',
    '2021-11-21 19:02:30.036349',
    '2021-11-21 19:02:32.036372'
]
timestamps = [datetime.fromisoformat(s) for s in timestrings]

ch4Ref = [
    5,
    5,
    5,
    5,
    5,
    5,
    5,
    5
]

ms = MeasurementServer()
# ms.createSeries("Test with new names")
# ms.runMeasurement(10, 1, 'With new names 2')
# print(ms.getSeriesList())
# ms.uploadReferenceData(6, timestamps, ch4Ref)
ms.startCalibration("Test",6,6)

# pmc = PyroMeasurementClient()
# print(pmc.getServerStatus())
# print(pmc.getSeriesList())
# pmc.runMeasurement(10, 1, 'TTTT')
# pmc.createSeries('With sensor',MeasureType.COMMON)
# print(pmc.getSeriesList())
