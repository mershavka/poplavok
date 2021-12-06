from django import forms
from django.db.models import fields
from django.forms.fields import CharField, ChoiceField, FloatField
from .models import MeasurmentSeries, Measurement
from measurementServer.common import MeasureType

class CreateSeriesForm(forms.Form):
    name=CharField(max_length=50, label="Описание")
    type=ChoiceField(label="Тип серии", choices=MeasureType.getList())


class CreateMeasurementSeriesForm(forms.ModelForm):
    class Meta:
        model = MeasurmentSeries
        fields = ['name', 'description', 'type']

class StartExperimentForm(forms.Form):
    name=CharField(max_length=50)
    period=FloatField(initial=1.0)
    duration=FloatField(initial=10.0)
