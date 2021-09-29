from enums import MeasureType
from measurmentserver import MeasurementServer
from measurement import Measurement
from series import Series
from referenceData import ReferenceData
import Pyro4
import Pyro4.util
import Pyro4.naming

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class PyroMeasurementServer(object):
    
    def __init__(self):
        self.ms = MeasurementServer()
    
    def createSeries(self, description, type):
        return self.ms.createSeries(description, type)
    
    def chooseSeries(self, seriesId):
        return self.ms.chooseSeries(seriesId)

    def addReferenceDataToSeries(self, path):
        return self.ms.addReferenceDataToSeries(path)

    def runMeasurement(self, type, duration, periodicity, description):
        return self.ms.runMeasurement(MeasureType(type), duration, periodicity, description)

    def interruptMeasurement(self):
        return self.ms.interruptMeasurement()

    def chooseMeasurement(self, id):
        return self.ms.chooseMeasurement(id)

    def getCurrentMeasurement(self):
        return self.ms.getCurrentMeasurement()

    def deleteCurrentMeasurement(self):
        return self.ms.deleteCurrentMeasurement()

    def getServerStatus(self):
        return self.ms.getServerStatus()

    def getCurrentSeries(self):
        return self.ms.getCurrentSeries()
    
    def getSeriesList(self):
        return self.ms.getSeriesList()

    def startCalibration(self, seriesIdStep1, seriesIdStep2):
        return self.ms.startCalibration(seriesIdStep1, seriesIdStep2)

    def selectCH4Model(self, id):
        return self.ms.selectCH4Model(id)

    def helloString(self):
        return "Hello!"

Pyro4.util.SerializerBase.register_class_to_dict(Series, Series.toJsonString)
Pyro4.util.SerializerBase.register_class_to_dict(Measurement, Measurement.toJsonString)
Pyro4.util.SerializerBase.register_class_to_dict(ReferenceData, ReferenceData.toJsonString)

Pyro4.util.SerializerBase.register_dict_to_class(Series, Series.fromJson)
Pyro4.util.SerializerBase.register_dict_to_class(Measurement, Measurement.fromJson)
Pyro4.util.SerializerBase.register_dict_to_class(ReferenceData, ReferenceData.fromJson)

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