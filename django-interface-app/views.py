from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .forms import CreateMeasurementSeriesForm, StartExperimentForm
from django.urls import reverse
from datetime import datetime
import measurementServer.pyroMeasurementClient as pmc


# Create your views here.

def index(request):
    return render(request, 'index.html')

def index_data(request):
    # here you return whatever data you need updated in your template
    now = datetime.now()
    server_time = dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    # device_status = 'init'
    device_status = pmc.pyro_measurement_server.getServerStatus()
    pressure = 0
    temperature = 20
    humidity = 40
    methane = 0

    return JsonResponse({
        'server_time'   : server_time,
        'device_status' : device_status,
        'pressure'      : pressure,
        'temperature'   : temperature,
        'humidity'      : humidity,
        'methane'       : methane,
    })

def stopExperiment(request):
    return render(request, 'index.html')

def createSeries(request):
    if request.method == 'POST':
        form = CreateMeasurementSeriesForm(request.POST)

        return HttpResponseRedirect(reverse('index'))
    else:
        form  = CreateMeasurementSeriesForm()
    return render(request, 'createSeries.html', {'form': form})

def startExperiment(request):
    if request.method == 'POST':
        form = StartExperimentForm(request.POST)
        
        return HttpResponseRedirect(reverse('index'))
    else:
        form  = StartExperimentForm()
    return render(request, 'createSeries.html', {'form': form})
