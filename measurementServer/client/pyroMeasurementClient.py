import sys
import Pyro4
import Pyro4.util

from ..common import *
from ..pyro4iface import PyroMeasurementInterface

Pyro4.config.REQUIRE_EXPOSE = False

Pyro4.util.SerializerBase.register_class_to_dict(Series, Series.toDict)
Pyro4.util.SerializerBase.register_class_to_dict(Measurement, Measurement.toDict)
Pyro4.util.SerializerBase.register_class_to_dict(ReferenceData, ReferenceData.toDict)

Pyro4.util.SerializerBase.register_dict_to_class(Series, Series.fromJson)
Pyro4.util.SerializerBase.register_dict_to_class(Measurement, Measurement.fromJson)
Pyro4.util.SerializerBase.register_dict_to_class(ReferenceData, ReferenceData.fromJson)

class PyroMeasurementClient(PyroMeasurementInterface):

    __proxy_name = "PyroMeasurementServer"

    def __init__(self,host='localhost') -> None:
        sys.excepthook = Pyro4.util.excepthook
        nameserver = Pyro4.locateNS(host)
        uri = nameserver.lookup(self.__proxy_name)
        uri.host = host
        self.ms = Pyro4.Proxy(uri)    # use name server object lookup uri shortcut
        super().__init__(self.ms)













# print(pyro_measurement_server.getSeriesList())
# print(pyro_measurement_server.createSeries("Pyro test", MeasureType.COMMON))
# print(pyro_measurement_server.chooseSeries(1))
# print(pyro_measurement_server.addReferenceDataToSeries("C:/Users/mershavka/Repositories/poplavok-algorithm/sandbox/exp_2021_06_23_185934.csv"))
# print(pyro_measurement_server.getCurrentSeries())
# print(pyro_measurement_server.chooseMeasurement(2))
# print(pyro_measurement_server.getCurrentMeasurement())
# print(pyro_measurement_server.runMeasurement(MeasureType.COMMON, 5, 1, "Pyro test"))
# time.sleep(7)
# print(pyro_measurement_server.getServerStatus())
# print(pyro_measurement_server.deleteCurrentMeasurement())
