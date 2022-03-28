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
from django.contrib import messages
import csv
import pandas as pd

pmc = PyroMeasurementClient()

# Create your views here.

def index(request):
    try:
        currentSeries = pmc.getCurrentSeries()
    except Exception:
        return HttpResponseRedirect('unavailible')
    measurements = []
    plotValues = [  
        'lastTemp'    ,
        'lastPres'    ,
        'lastRHum'    ,
        'lastAHum'    ,
        'lastVolt'    ,
        'lastCH4'     ,
        'lastH2OppmM' ,
        'lastH2OppmV' 
    ]
    if not currentSeries is None:
        measurements = pmc.getMeasurementsList(currentSeries['id'])
    return render(request, 'index.html', {'measurements' : measurements, 'plotValues': plotValues})

def unavailible(request):
    if pmc.connect():
        return HttpResponseRedirect('/')
    else:
        return render(request, "unavailible.html")


def getStatus(request):
    # here you return whatever data you need updated in your template
    now = datetime.now()
    server_time = dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    # device_status = 'init'
    try:
        deviceStatus = pmc.getServerStatus()  
    except Exception:
        return HttpResponseRedirect('unavailible')
    deviceStatusString = deviceStatus[1]

    lastDataDict = pmc.getLastData()
    lastTime = lastDataDict[ValuesNames.timestamp.name]
    t = lastDataDict[ValuesNames.temperature.name]
    p = lastDataDict[ValuesNames.pressure.name]
    aH = lastDataDict[ValuesNames.aHumidity.name]
    rH = lastDataDict[ValuesNames.rHumidity.name]
    fanSpeed = lastDataDict[ValuesNames.fanSpeed.name]
    lastTemp = "{:2.2f}".format(t)
    lastPres = "{:4.2f}".format(p)
    lastRHum =  "{:2.2f}".format(rH)
    lastAHum =  "{:2.2f}".format(aH * 1000)
    lastVolt = "{:.3f}".format(lastDataDict[ValuesNames.voltage.name])
    lastCH4 = "{:.3f}".format(lastDataDict[ValuesNames.ch4.name]) if ValuesNames.ch4.name in lastDataDict.keys() else "-"
    lastH2OppmM = "{:.0f}".format(1000000 * aH / (aH + p*100*0.02897/8.31446261815324/(t+273)))
    lastH2OppmV = "{:.0f}".format(1000000 * aH / 0.01801528 / (aH/0.01801528 + p*100/8.31446261815324/(t+273)))
    
    currentSeriesString = pmc.getCurrentSeries()
    currentCalibrationString = pmc.getCurrentCalibration()
    if (currentSeriesString is None):
        currentSeriesString = "Серия не выбрана"
    else:
        currentSeriesString = str(currentSeriesString['id'])

    if (currentCalibrationString is None):
        currentCalibrationString = "Калибровка не выбрана"
    else:
        currentCalibrationString = str(currentCalibrationString['id'])

    return JsonResponse({
        'server_time'   : server_time,
        'device_status' : deviceStatusString,
        'current_series': currentSeriesString,
        'current_calibration': currentCalibrationString,
        'fanSpeed': fanSpeed,
        'lastTime': lastTime,
        'lastTemp' : lastTemp,
        'lastPres' : lastPres,
        'lastRHum':  lastRHum,
        'lastAHum':  lastAHum,
        'lastVolt': lastVolt,
        'lastCH4': lastCH4,
        'lastH2OppmM' : lastH2OppmM,
        'lastH2OppmV' : lastH2OppmV,
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
    seriesIdsWithRefData = pmc.getRefIdsList()  
    return render(request, 'series.html', {'series' : seriesList, "seriesIdsWithRefData" : seriesIdsWithRefData})

def seriesDetails(request, series_id):
    measurements = pmc.getMeasurementsList(series_id)
    return render(request, 'seriesDetails.html', {'series_id' : series_id, 'measurements' : measurements})

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
    seriesIdsWithRefData = pmc.getRefIdsList()
    seriesTuple = [(s['id'], "id = {} ({}, {})".format(s['id'],s['description'],s['date'])) for s in series]
    seriesTupleWithRefData = [(s['id'], "id = {} ({}, {})".format(s['id'],s['description'],s['date'])) for s in series if s['id'] in seriesIdsWithRefData]
    seriesTupleWithRefData.append((0, "Без второго шага"))

    if request.method == 'POST':
        form = StartCalibrationForm(seriesTuple, seriesTupleWithRefData, request.POST)

        series1Id = int(form.data['series1Id'])
        series2Id = int(form.data['series2Id'])
        if series2Id == 0:
            image_path = pmc.firstStepOfCalibration(series1Id)
            if os.path.exists(image_path):
                messages.info(request, 'Калибровка успешно проведена')        
                with open(image_path, 'rb') as img:
                    return HttpResponse(img.read(), content_type="image/png")
            messages.info(request, 'Что-то пошло не так')
        else:
            result = pmc.startCalibration(series1Id, series2Id)

    else:
        form = StartCalibrationForm(seriesTuple, seriesTupleWithRefData)
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

def downloadPlot(request, series_id, measurement_id, var_name):
    image_path = pmc.plotMeasurement(variable=var_name, series_id=series_id, measurement_id=measurement_id)
    if not image_path:
        return HttpResponse('Не удалось построить график. Проверьте, что данные существуют')
    if os.path.exists(image_path):
        with open(image_path, 'rb') as img:
            response = HttpResponse(img.read(), content_type="image/png")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(image_path) + '.png'
            return response

def handle_uploaded_file(f):
    with open('file.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def setFansSpeed(request, speed):
    if speed > 100 or speed < 0:
        pmc.setFansSpeed(0)
        return JsonResponse(
            {
                'status' : 0
            })
    pmc.setFansSpeed(speed)
    return JsonResponse(
        {
            'status' : 1
        }
    )


def uploadReferenceData(request, series_id):
    if request.method == 'POST':
        form = UploadRefDataForm(request.POST, request.FILES)
        if form.is_valid():
            refDataFile = request.FILES['referenceDataFile']
            if not refDataFile.content_type in ['text/csv', 'application/vnd.ms-excel']:
                messages.error(request, "Референсные данные должны быть в формате CSV, получен файл формата {}".format(refDataFile.content_type))
            else:    
                messages.info(request, 'Получен файл {}, {:.2f} Мб'.format(refDataFile.name, refDataFile.size / 1024**2))
                refDataPath = "veryStrangeFile.csv"
                with open(refDataPath, "wb+") as destination:
                    for chunk in refDataFile.chunks():
                        destination.write(chunk)
                if os.path.exists(refDataPath):
                    column_names = ["Timestamp", "Reference Methane Concentration, ppm"]
                    df = pd.read_csv(refDataPath, delimiter=',', names=column_names)
                    if len(df.columns) == 2:
                        timestampsList = df[column_names[0]].tolist()
                        ch4RefList = df[column_names[1]].tolist()
                        if pmc.uploadReferenceData(series_id, timestampsList, ch4RefList):
                            messages.info(request, "Данные успешно загружены")
                    os.remove(refDataPath)

    else:
        form = UploadRefDataForm()
    return render(request, 'uploadReferenceData.html', {'form' : form, "series_id" : series_id})