from django import forms
from .models import Accident

class AccidentForm(forms.ModelForm):
    class Meta:
        model = Accident
        fields = '__all__'

        widgets = {
            'accident_date': forms.SelectDateWidget(years=range(2000, 2026)),
        }