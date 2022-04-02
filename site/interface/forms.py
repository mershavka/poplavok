from django import forms
from django.db.models import fields
from django.forms.fields import CharField, ChoiceField, FileField, FloatField, IntegerField
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


from .models import MeasurmentSeries, Measurement
from measurementServer.common import MeasureType

class CreateSeriesForm(forms.Form):
    name=CharField(max_length=500, label="Описание")
    type=ChoiceField(label="Тип серии", choices=MeasureType.getList())


class CreateMeasurementSeriesForm(forms.ModelForm):
    class Meta:
        model = MeasurmentSeries
        fields = ['name', 'description', 'type']

class StartExperimentForm(forms.Form):
    name=forms.CharField(max_length=500, label = "Описание")
    period=forms.FloatField(min_value=0.0, initial=1.0, label = "Периодичность измерений")
    duration=forms.FloatField(min_value=0.0, initial=10.0, label = "Длительность измерения")

    def __init__(self, choicesList, *args, **kwargs):
        super(StartExperimentForm, self).__init__(*args, **kwargs)
        self.fields['seriesId'] = forms.ChoiceField(label="Серия",
            choices=choicesList
        )

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
        self.file = forms.FileField(label="Референсные данные", validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    def validate_file_extension(self):
        valid_extensions = ['text/csv']
        if not self.file.content_type in valid_extensions:
            print("Your file must be a CSV type")
            raise ValidationError(u'Error message')

        
