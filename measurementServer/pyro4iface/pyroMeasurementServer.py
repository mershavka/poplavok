from measurementServer.server import MeasurementServer
from .pyroMeasurementInterface import PyroMeasurementInterface
import Pyro4
import Pyro4.util

Pyro4.config.REQUIRE_EXPOSE = False

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class PyroMeasurementServer(PyroMeasurementInterface):
    
    def __init__(self):        
        self.ms = MeasurementServer()
        super().__init__(self.ms)



# daemon = Pyro4.Daemon()
# ns = Pyro4.locateNS()                  # find the name server
# uri = daemon.register(PyroMeasurementServer)   # register the greeting maker as a Pyro object
# ns.register("PyroMeasurementServer", uri)   # register the object with a name in the name server

# print("Ready. Object uri =", uri)
# daemon.requestLoop()