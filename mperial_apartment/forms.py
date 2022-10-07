from dataclasses import field
from django.forms import ModelForm
from .models import Flat


class FlatForm(ModelForm):
    class Meta:
        model = Flat
        field = '__all__'
        
form = FlatForm()
