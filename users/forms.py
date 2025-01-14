from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import get_user_model


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=100, required=True)
    is_staff = forms.BooleanField(required=False, initial=True, widget=forms.HiddenInput)
    is_superuser = forms.BooleanField(required=False, initial=True, widget=forms.HiddenInput)
    class Meta:
        fields = ('username', 'phone_number', 'address', 'password1', 'password2', 'is_staff', 'is_superuser')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'})
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        user.address = self.cleaned_data['address']
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user