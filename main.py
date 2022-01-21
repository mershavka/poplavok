from measurementServer import calibration
from measurementServer.client import PyroMeasurementClient
# from measurementServer.common import *
from measurementServer.common.enums import MeasureType
from measurementServer.server import MeasurementServer
from datetime import datetime
import traceback
import warnings
from time import sleep
from measurementServer.drivers import driver

mbDriver = driver.Driver()
mbDriver.open()
print(mbDriver.readData())
# mbDriver.pca_turn_fan_on(0)
mbDriver.pca_set_led0(1)

# mbDriver.pca_control_fan(fan_id = 9, dutycycle = 70, delay = 0)
# mbDriver.pca_control_fan(fan_id = 1, dutycycle = 100, delay = 0)
# sleep(5)

# mbDriver.pca_control_fan(fan_id = 0, dutycycle = 50, delay = 0)
# mbDriver.pca_control_fan(fan_id = 9, dutycycle = 50, delay = 0)
# sleep(5)

# mbDriver.pca_control_fan(fan_id = 0, dutycycle = 20, delay = 0)
# mbDriver.pca_control_fan(fan_id = 9, dutycycle = 20, delay = 0)
# sleep(5)
# mbDriver.pca_turn_fan_off(0)
# mbDriver.pca_turn_fan_off(0)

# ms = MeasurementServer()
# logger = ms.getLogger()
# ms.getServerStatus()
# ms.chooseSeries(3)
# ms.createSeries("Test with generated data")
# ms.runMeasurement(10, 1, 'Check CH4')
# print(ms.getSeriesDict())
# print(ms.getRefDatas())
# ms.startRecalibration(seriesId=2, refDataId=2, calibrationId = 1)
# print(ms.getSeriesList())
# ms.uploadReferenceData(2, timestamps, ch4Ref)
# try:
# ms.startCalibration(seriesIdStep1=1,seriesIdStep2=2)
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
# pmc.startCalibration(1,2)
# print(pmc.getSeriesPath(id))
# print(pmc.getCurrentSeries())
# print(pmc.getSeriesList())
# pmc.runMeasurement(10, 1, 'TTTT')
# pmc.createSeries('With sensor',MeasureType.COMMON)
# print(pmc.getSeriesList())
