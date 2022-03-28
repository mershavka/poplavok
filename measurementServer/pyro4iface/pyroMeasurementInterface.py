from ..common import *

class PyroMeasurementInterface(object):
    
    def __init__(self, ms ):
        self.ms = ms
    
    def createSeries(self, description, type):
        return self.ms.createSeries(description, type)
    
    def chooseSeries(self, seriesId):
        return self.ms.chooseSeries(seriesId)

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

    def getSeriesById(self, id):
        return self.ms.getSeriesById(id)

    def getSeriesPath(self, id):
        return self.ms.getSeriesPath(id)

    def getMeasurementsList(self, seriesId):
        return self.ms.getMeasurementsList(seriesId)

    def getMeasurementPath(self, seriesId, measurementId):
        return self.ms.getMeasurementPath(seriesId, measurementId)

    def startCalibration(self, seriesIdStep1, seriesIdStep2):
        return self.ms.startCalibration(seriesIdStep1, seriesIdStep2)

    def firstStepOfCalibration(self, seriesIdStep1):
        return self.ms.firstStepOfCalibration(seriesIdStep1)
    
    def getLastData(self):
        return self.ms.getLastData()

    def uploadReferenceData(self, seriesId, timestampsList, ch4RefList):
        return self.ms.uploadReferenceData(seriesId, timestampsList, ch4RefList)

    def getReferenceDataPath(self):
        return self.ms.getReferenceDataPath()

    def getRefIdsList(self):
        return self.ms.getRefIdsList()

    def chooseCalibration(self, id):
        return self.ms.chooseCalibration(id)

    def getCurrentCalibration(self):
        return self.ms.getCurrentCalibration()
    
    def getCalibrationsList(self):
        return self.ms.getCalibrationsList()
    
    def setFansSpeed(self, speed):
        return self.ms.setFansSpeed(speed)

    def plotMeasurement(self, variable, series_id, measurement_id):
        return self.ms.plotMeasurement(variable, series_id, measurement_id)
