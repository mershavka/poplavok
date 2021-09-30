from measurementServer.pyro4iface import PyroMeasurementClient

pmc = PyroMeasurementClient()
print(pmc.getServerStatus())
