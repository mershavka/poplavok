import argparse
import Pyro4
import Pyro4.naming
from measurementServer.server import PyroMeasurementServer

ap = argparse.ArgumentParser(description='Measurement Server')

ap.add_argument("-p", "--port", required=False, default=52603, help="Port of Measurement Server")
ap.add_argument("-H", "--host", required=False, default='localhost', help="Host of Measurement Server")
args = vars(ap.parse_args())

host = str(args['host'])
port = int(args['port'])

# Pyro4.naming.startNS()
Pyro4.Daemon.serveSimple(
            {
                PyroMeasurementServer: "PyroMeasurementServer"                
            }, 
            host    = host,         
            port    = port,
            ns      = True,
            verbose = True
            )