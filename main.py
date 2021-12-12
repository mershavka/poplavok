from measurementServer.client import PyroMeasurementClient
# from measurementServer.common import *
from measurementServer.common.enums import MeasureType
from measurementServer.server import MeasurementServer
from datetime import datetime
import traceback
import warnings


ms = MeasurementServer()
logger = ms.getLogger()
# ms.getServerStatus()
# ms.chooseSeries(3)
# ms.createSeries("Test with generated data")
# ms.runMeasurement(10, 1, 'Check CH4')
# print(ms.getSeriesDict())

# print(ms.getSeriesList())
# ms.uploadReferenceData(2, timestamps, ch4Ref)
# try:
# 	ms.startCalibration(seriesIdStep1=1,seriesIdStep2=2)
# except Warning as w:
# 	logger.warning(w)
# 	print(traceback.format_exc())
# except Exception as e:
# 	logger.exception(e, exc_info=True)

# ms.ma.generateTestDatasets(measuresCount=200,step=2)
# ms.createSeries('Battle Series', MeasureType.EXPERIMENT)
# ms.chooseCalibration(2)
# ms.runMeasurement(10, 1, 'Hello')

# pmc = PyroMeasurementClient()
# print(pmc.getSeriesPath(id))
# print(pmc.getCurrentSeries())
# print(pmc.getSeriesList())
# pmc.runMeasurement(10, 1, 'TTTT')
# pmc.createSeries('With sensor',MeasureType.COMMON)
# print(pmc.getSeriesList())
