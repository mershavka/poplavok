from ..common import *

class PyroMeasurementInterface(object):
    
    def __init__(self, ms):
        self.ms = ms
    
    def createSeries(self, description, type):
        return self.ms.createSeries(description, type)
    
    def chooseSeries(self, seriesId):
        return self.ms.chooseSeries(seriesId)

    def addReferenceDataToSeries(self, path):
        return self.ms.addReferenceDataToSeries(path)

    def runMeasurement(self, duration, periodicity, description):
        return self.ms.runMeasurement(duration, periodicity, description)

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

    def getMeasurementsList(self, seriesId):
        return self.ms.getMeasurementsList(seriesId)

    def startCalibration(self, seriesIdStep1, seriesIdStep2):
        return self.ms.startCalibration(seriesIdStep1, seriesIdStep2)

    def selectCH4Model(self, id):
        return self.ms.selectCH4Model(id)

    # def helloString(self):
    #     return "Hello!"