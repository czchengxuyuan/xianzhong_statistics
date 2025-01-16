from django import forms
from .models import Accident

class AccidentForm(forms.ModelForm):
    class Meta:
        model = Accident
        fields = ('address','accident_date','description','accident_type','injured','dead','unknown')

        widgets = {
            'accident_date': forms.SelectDateWidget(years=range(2000, 2026)),
        }

    address = forms.CharField(max_length=255, widget=forms.HiddenInput())