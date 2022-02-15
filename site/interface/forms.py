from django import forms
from django.db.models import fields
from django.forms.fields import CharField, ChoiceField, FileField, FloatField, IntegerField
from django.core.exceptions import ValidationError

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

class StartCalibrationForm(forms.Form):

    def __init__(self, choicesList1, choicesList2, *args, **kwargs):
        super(StartCalibrationForm, self).__init__(*args, **kwargs)
        self.fields['series1Id'] = forms.ChoiceField(label="Id серии 1 шаг",
            choices=choicesList1
        )
        self.fields['series2Id'] = forms.ChoiceField(label="Id серии 2 шаг",
            choices=choicesList2
        )

class UploadRefDataForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UploadRefDataForm, self).__init__(*args, **kwargs)
        self.file = forms.FileField(label="Референсные данные", validators=[self.validate_file_extension])
    def validate_file_extension(self):
        valid_extensions = ['application/pdf','application/doc','application/docx']
        if not self.file.content_type in valid_extensions:
            raise ValidationError(u'Error message')

        
