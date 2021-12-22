from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('startCalibration', views.startCalibration),
    path('startExperiment', views.startExperiment),
    path('stopExperiment', views.stopExperiment),
    path('createSeries', views.createSeries),
    path('series', views.series),
    path('seriesDetails/<int:series_id>', views.seriesDetails),
    path('getStatus', views.getStatus, name='getStatus'),
    path('chooseSeries/<int:series_id>', views.chooseSeries),
    path('downloadSeries/<int:series_id>', views.downloadSeries),
    path('uploadReferenceData/<int:series_id>', views.uploadReferenceData),
    path('calibrations', views.calibrations)
]