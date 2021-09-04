import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class PyroMeasurementServer(object):
    
    def helloString(self):
        return "Hello!"

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