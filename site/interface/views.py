from json.decoder import JSONDecodeError
from Pyro4.util import reset_exposed_members
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, Http404
from django.views.generic import TemplateView
from measurementServer.common.enums import Status
from .forms import CreateSeriesForm, StartExperimentForm, StartCalibrationForm, UploadRefDataForm
from django.urls import reverse
from django.shortcuts import redirect
from datetime import datetime
from measurementServer.client import PyroMeasurementClient
from measurementServer.common import ValuesNames
from zipfile import ZipFile, ZIP_DEFLATED
import os
import json



pmc = PyroMeasurementClient()

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
    lastTime = lastDataDict[ValuesNames.timestamp.name]
    lastTemp = "{:2.2f}".format(lastDataDict[ValuesNames.temperature.name])
    lastPres = "{:4.2f}".format(lastDataDict[ValuesNames.pressure.name])
    lastHum =  "{:2.2f}".format(lastDataDict[ValuesNames.rHumidity.name])

    
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

def calibrations(request):
    calibrationList = pmc.getCalibrationsList()
    return JsonResponse(json.dumps(calibrationList))
    # return render(request, 'calibrations.html', {'calibrations' : calibrationList})

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

def startCalibration(request):
    
    series = pmc.getSeriesList()
    seriesTuple = [(s['id'], "id = {} ({}, {})".format(s['id'],s['description'],s['date'])) for s in series] 

    if request.method == 'POST':
        form = StartCalibrationForm(seriesTuple, request.POST)

        series1Id = form.data['series1Id']
        series2Id = form.data['series2Id']
        pmc.startCalibration(series1Id, series2Id)

    else:
        form = StartCalibrationForm(seriesTuple)
    return render(request, 'startCalibration.html', {'form' : form})

def zipfolder(foldername, target_dir):            
    zipobj = ZipFile(foldername, 'w', ZIP_DEFLATED)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for file in files:
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])

def downloadSeries(request, series_id):
    series_folder_path = pmc.getSeriesPath(series_id)    
    zippath = 'series'+str(series_id) + '.zip'
    zipfolder(zippath, series_folder_path)  
    if os.path.exists(zippath):
        with open(zippath, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/zip")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(series_folder_path) + '.zip'
            return response
    os.remove(zippath)
    raise Http404

def handle_uploaded_file(f):
    with open('file.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def uploadReferenceData(request, series_id):
    series = pmc.getSeriesList()
    if request.method == 'POST':
        # form = UploadRefDataForm(request.POST)
        # refData = form.data["referenceData"]
        print(request)
        print(request.FILES)
        handle_uploaded_file(request.FILES['referenceDataFile'])
        # pmc.uploadReferenceData(series_id, refData)
    else:
        form = UploadRefDataForm()
    return redirect('/series') 