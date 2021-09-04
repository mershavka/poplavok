import sys
import Pyro4
import Pyro4.util

sys.excepthook = Pyro4.util.excepthook
pyro_measurement_server = Pyro4.Proxy("PYRONAME:PyroMeasurementServer")    # use name server object lookup uri shortcut
# uri = input("Enter the uri of the warehouse: ").strip()
# pyro_measurement_server = Pyro4.Proxy(uri)
print(pyro_measurement_server.helloString())