import sys
from tkinter.tix import Tree
import Pyro4
import Pyro4.util

from ..common import *
from ..pyro4iface import PyroMeasurementInterface
from ..calibration import CalibrationResult

Pyro4.config.REQUIRE_EXPOSE = False

Pyro4.util.SerializerBase.register_class_to_dict(Series, Series.toDict)
Pyro4.util.SerializerBase.register_class_to_dict(Measurement, Measurement.toDict)
Pyro4.util.SerializerBase.register_class_to_dict(ReferenceData, ReferenceData.toDict)
Pyro4.util.SerializerBase.register_class_to_dict(CalibrationResult, CalibrationResult.toDict)

Pyro4.util.SerializerBase.register_dict_to_class(Series, Series.fromJson)
Pyro4.util.SerializerBase.register_dict_to_class(Measurement, Measurement.fromJson)
Pyro4.util.SerializerBase.register_dict_to_class(ReferenceData, ReferenceData.fromJson)
Pyro4.util.SerializerBase.register_dict_to_class(CalibrationResult, CalibrationResult.fromJson)

class PyroMeasurementClient(PyroMeasurementInterface):

    __proxy_name = "PyroMeasurementServer"

    def __init__(self) -> None:        
        self.connect()        
    
    def connect(self):
        try:
            sys.excepthook = Pyro4.util.excepthook
            nameserver = Pyro4.locateNS()
            uri = nameserver.lookup(self.__proxy_name)
            self.ms = Pyro4.Proxy(uri)    # use name server object lookup uri shortcut
            self.ms._pyroBind()
            super().__init__(self.ms)
            self.connected = True
            return True
        except Exception:
            self.ms = None
            return False
    
    def checkConnection(self) -> bool:
        try:
            self.ms.getServerStatus()
        except Pyro4.errors.CommunicationError:
            self.connected = False
            self.ms = None
            return False
        return True
