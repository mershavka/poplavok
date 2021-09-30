import Pyro4
from measurementServer.pyro4iface import PyroMeasurementServer

Pyro4.Daemon.serveSimple(
            {
                PyroMeasurementServer: "PyroMeasurementServer"
            },
            ns = True)