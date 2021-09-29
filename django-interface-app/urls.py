from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('startExperiment', views.startExperiment),
    path('stopExperiment', views.stopExperiment),
    path('createSeries', views.createSeries),
    path('index_data', views.index_data, name='index_data'),
]