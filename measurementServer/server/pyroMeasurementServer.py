import Pyro4
import Pyro4.util
import os

from . import MeasurementServer
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

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class PyroMeasurementServer(PyroMeasurementInterface):
    
    def __init__(self):
        path = os.getenv('PYRO_MS_DATA_PATH')
        if path is None:
            path = './MS_DATA'
        mode = os.getenv('PYRO_MS_MODE')  
        if mode is None:
            mode = True
        else:
            mode = False if mode=='False' else True
        self.ms = MeasurementServer(path, mode)
        super().__init__(self.ms)



# daemon = Pyro4.Daemon()
# ns = Pyro4.locateNS()                  # find the name server
# uri = daemon.register(PyroMeasurementServer)   # register the greeting maker as a Pyro object
# ns.register("PyroMeasurementServer", uri)   # register the object with a name in the name server

# print("Ready. Object uri =", uri)
# daemon.requestLoop()