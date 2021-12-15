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

    def __init__(self) -> None:
        sys.excepthook = Pyro4.util.excepthook
        nameserver = Pyro4.locateNS()
        uri = nameserver.lookup(self.__proxy_name)
        self.ms = Pyro4.Proxy(uri)    # use name server object lookup uri shortcut
        super().__init__(self.ms)
