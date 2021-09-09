from measurmentserver import MeasurementServer
from measurement import Measurement
from series import Series
import Pyro4
import Pyro4.util

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class PyroMeasurementServer(object):
    
    def __init__(self):
        self.ms = MeasurementServer()
    
    def createSeries(self, description, type):
        return self.ms.createSeries(description, type)
    
    def chooseSeries(self, id):
        return self.ms.chooseSeries(id)

    def runMeasurement(self, type, duration, periodicity, description):
        return self.ms.runMeasurement(type, duration, periodicity, description)

    def getServerStatus(self):
        return self.ms.getServerStatus()
    
    def getSeriesList(self):
        return self.ms.getSeriesList()

    def helloString(self):
        return "Hello!"

Pyro4.util.SerializerBase.register_class_to_dict(Series, Series.toJson)
Pyro4.util.SerializerBase.register_class_to_dict(Measurement, Measurement.toJson)
Pyro4.util.SerializerBase.register_dict_to_class(Series, Series.fromJson)
Pyro4.util.SerializerBase.register_dict_to_class(Measurement, Measurement.fromJson)

Pyro4.Daemon.serveSimple(
            {
                PyroMeasurementServer: "PyroMeasurementServer"
            },
            ns = True)

# daemon = Pyro4.Daemon()
# ns = Pyro4.locateNS()                  # find the name server
# uri = daemon.register(PyroMeasurementServer)   # register the greeting maker as a Pyro object
# ns.register("PyroMeasurementServer", uri)   # register the object with a name in the name server

# print("Ready. Object uri =", uri)
# daemon.requestLoop()