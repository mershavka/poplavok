from Pyro4.util import reset_exposed_members
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView
from .forms import CreateSeriesForm, StartExperimentForm
from django.urls import reverse
from datetime import datetime
from measurementServer.pyro4iface import PyroMeasurementClient


pmc = PyroMeasurementClient()

# Create your views here.

def index(request):
    seriesListString = pmc.getSeriesList()
    return render(request, 'index.html', {'seriesList' : seriesListString})

def index_data(request):
    # here you return whatever data you need updated in your template
    now = datetime.now()
    server_time = dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    # device_status = 'init'
    device_status = pmc.getServerStatus()
    current_series = pmc.getCurrentSeries()
    pressure = 0
    temperature = 20
    humidity = 40
    methane = 0

    return JsonResponse({
        'server_time'   : server_time,
        'device_status' : device_status,
        'current_series': current_series,
        'pressure'      : pressure,
        'temperature'   : temperature,
        'humidity'      : humidity,
        'methane'       : methane,
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

def seriesList(request):
    seriesListString = pmc.getSeriesList()
    
    return render(request, 'seriesList.html', {'seriesList' : seriesListString})

def startExperiment(request):
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
