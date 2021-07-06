from measurmentserver import MeasurementServer, Status

ms = MeasurementServer()

ms.createSeries("Test Series", "Series for test")

# ms.startMeasurements("1.csv", 10, 1)

# while (ms.status != Status.NO):
# 	pass

# print('Experiment is over!')
