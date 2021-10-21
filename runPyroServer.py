import Pyro4
from measurementServer.server import PyroMeasurementServer

Pyro4.Daemon.serveSimple(
            {
                PyroMeasurementServer: "PyroMeasurementServer"
            },
            ns = True)