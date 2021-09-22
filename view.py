import enum
from series import Series
import sys
import Pyro4
import Pyro4.util
from enums import *
from series import Series
from measurement import Measurement
from referenceData import ReferenceData
import time

Pyro4.util.SerializerBase.register_class_to_dict(Series, Series.toJson)
Pyro4.util.SerializerBase.register_class_to_dict(Measurement, Measurement.toJson)
Pyro4.util.SerializerBase.register_class_to_dict(ReferenceData, ReferenceData.toJson)

Pyro4.util.SerializerBase.register_dict_to_class(Series, Series.fromJson)
Pyro4.util.SerializerBase.register_dict_to_class(Measurement, Measurement.fromJson)
Pyro4.util.SerializerBase.register_dict_to_class(ReferenceData, ReferenceData.fromJson)

sys.excepthook = Pyro4.util.excepthook
pyro_measurement_server = Pyro4.Proxy("PYRONAME:PyroMeasurementServer")    # use name server object lookup uri shortcut
# print(pyro_measurement_server.getSeriesList())
# print(pyro_measurement_server.createSeries("Pyro test", MeasureType.COMMON))
print(pyro_measurement_server.chooseSeries(1))
# print(pyro_measurement_server.addReferenceDataToSeries("C:/Users/mershavka/Repositories/poplavok-algorithm/sandbox/exp_2021_06_23_185934.csv"))
# print(pyro_measurement_server.getCurrentSeries())
# print(pyro_measurement_server.chooseMeasurement(2))
# print(pyro_measurement_server.getCurrentMeasurement())
# print(pyro_measurement_server.runMeasurement(MeasureType.COMMON, 5, 1, "Pyro test"))
# time.sleep(7)
print(pyro_measurement_server.getServerStatus())
# print(pyro_measurement_server.deleteCurrentMeasurement())
