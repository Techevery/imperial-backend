from django import forms
from .models import Property

class AddPropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
