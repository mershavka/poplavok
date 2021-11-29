from Pyro4.util import reset_exposed_members
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView
from measurementServer.common.enums import Status
from .forms import CreateSeriesForm, StartExperimentForm
from django.urls import reverse
from django.shortcuts import redirect
from datetime import datetime
from measurementServer.client import PyroMeasurementClient
from measurementServer.common import ValuesNames


pmc = PyroMeasurementClient('host.docker.internal')

# Create your views here.

def index(request):
    currentSeries = pmc.getCurrentSeries()
    measurements = []
    if not currentSeries is None:
        measurements = pmc.getMeasurementsList(currentSeries['id'])
    return render(request, 'index.html', {'measurements' : measurements})

def getStatus(request):
    # here you return whatever data you need updated in your template
    now = datetime.now()
    server_time = dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    # device_status = 'init'
    deviceStatus = pmc.getServerStatus()  
    deviceStatusString = deviceStatus[1]

    lastDataDict = pmc.getLastData()
    lastTime = lastDataDict[ValuesNames.timeString]
    lastTemp = "{:2.2f}".format(lastDataDict[ValuesNames.temperatureString])
    lastPres = "{:4.2f}".format(lastDataDict[ValuesNames.pressureString])
    lastHum =  "{:2.2f}".format(lastDataDict[ValuesNames.rHumidityString])

    
    currentSeriesString = pmc.getCurrentSeries()    
    if (currentSeriesString is None):
        currentSeriesString = "Серия не выбрана"
    else:
        currentSeriesString = str(currentSeriesString['id'])

    return JsonResponse({
        'server_time'   : server_time,
        'device_status' : deviceStatusString,
        'current_series': currentSeriesString,
        'lastTime': lastTime,
        'lastTemp' : lastTemp,
        'lastPres' : lastPres,
        'lastHum':  lastHum
    })

def stopExperiment(request):
    pmc.interruptMeasurement()
    return index(request)

def createSeries(request):
    if request.method == 'POST':
        form = CreateSeriesForm(request.POST)

        name = form.data['name']
        measureType = int(form.data['type'])
        pmc.createSeries(name, measureType)

        return HttpResponseRedirect(reverse('index'))
    else:
        form  = CreateSeriesForm()
    return render(request, 'createSeries.html', {'form': form})

def series(request):
    seriesList = pmc.getSeriesList()    
    return render(request, 'series.html', {'series' : seriesList})

def chooseSeries(request, series_id=0):
    if series_id != 0:
        pmc.chooseSeries(series_id) 
    return redirect('/series')

def startExperiment(request):
    currentSeries = pmc.getCurrentSeries()
    if currentSeries is None:
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        form = StartExperimentForm(request.POST)

        name        = form.data['name']
        period      = float(form.data['period'])
        duration    = float(form.data['duration'])
        pmc.runMeasurement(duration, period, name)

        return HttpResponseRedirect(reverse('index'))
    else:
        form  = StartExperimentForm()
    return render(request, 'createSeries.html', {'form': form})
