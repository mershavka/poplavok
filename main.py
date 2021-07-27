from measurmentserver import MeasurementServer, Status
from enums import MeasureType

ms = MeasurementServer()

MeasurementServer.testMode = True

seriesInfoJson = ms.createSeries(description="Test Series", type=MeasureType.COMMON)

ms.runMeasurement(duration=20, periodicity=2, description="Test measurement", type=MeasureType.COMMON)

while (ms.getStatus() != Status.NO):
	pass

print('Experiment is over!')
