from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('startExperiment', views.startExperiment),
    path('stopExperiment', views.stopExperiment),
    path('createSeries', views.createSeries),
    path('series', views.series),
    path('getStatus', views.getStatus, name='getStatus'),
    path('chooseSeries/<int:series_id>', views.chooseSeries)
]