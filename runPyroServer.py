import Pyro4
import Pyro4.naming
from measurementServer.server import PyroMeasurementServer


# Pyro4.naming.startNS()
Pyro4.Daemon.serveSimple(
            {
                PyroMeasurementServer: "PyroMeasurementServer"                
            },            
            port=52603,
            ns = True)