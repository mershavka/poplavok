from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('startCalibration', views.startCalibration, name='startCalibration'),
    path('startExperiment', views.startExperiment),
    path('stopExperiment', views.stopExperiment),
    path('createSeries', views.createSeries),
    path('series', views.series, name='series'),
    path('seriesDetails/<int:series_id>', views.seriesDetails, name='seriesDetails'),
    path('getStatus', views.getStatus, name='getStatus'),
    path('chooseSeries/<int:series_id>', views.chooseSeries),
    path('downloadSeries/<int:series_id>', views.downloadSeries, name='downloadSeries'),
    path('uploadReferenceData/<int:series_id>', views.uploadReferenceData),
    path('calibrations', views.calibrations),
    path('unavailible', views.unavailible),
	path('setFansSpeed/<int:speed>/', views.setFansSpeed, name='setFansSpeed')
]