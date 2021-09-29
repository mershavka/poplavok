from enum import Enum
from django.db import models
from django.db.models.fields import FilePathField

# class MeasurmentSeries(models.Model):
#     class SeriesType(models.TextChoices):
#         COMMON      = "COMMON"
#         EXPERIMENT  = "EXPERIMENT"
#         CALIB1      = "CALIB1"
#         CALIB2      = "CALIB2"

#     date = models.DateTimeField('Creation date', auto_now_add=True)
#     name = models.CharField(max_length=100, default='Series')
#     description = models.TextField()
#     type = models.CharField(max_length=30, choices=SeriesType.choices)
#     path = models.FilePathField()

# class Measurement(models.Model):
#     class MeasurementStatus(models.TextChoices):
#         CREATED     = "CREATED"
#         ACTIVE      = "ACTIVE"
#         FINISHED    = "FINISHED"
#         INTERRUPTED = "INTERRUPTED"
#         ERROR       = "ERROR"

#     name = models.CharField(max_length=100, default='Series')
#     start_date = models.DateTimeField('Start date', auto_now_add=True)
#     duration = models.IntegerField(default=10)
#     periodMeasure = models.FloatField(default=1.0)
#     status = models.CharField(max_length=30, choices=MeasurementStatus.choices)
#     filepath = models.FilePathField()
#     series = models.ForeignKey(MeasurmentSeries, on_delete=models.CASCADE)