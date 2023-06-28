from django import forms
from api.models import Property, Flat
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from django.forms import ModelMultipleChoiceField
from django.contrib.auth import get_user_model


class FlatForm(forms.ModelForm):
    class Meta:
        model = Flat
        fields = [
            'name',
            'number_of_rooms',
            'number_of_living_rooms',
            'number_of_kitchens',
            'number_of_toilets',
            'description',
        ]

class PropertyForm(forms.ModelForm):
    new_flat = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    flat_form = FlatForm()

    class Meta:
        model = Property
        fields = [
            'property_image',
            'property_name',
            'address',
            'flats',
            'user',
            'all_managers',
            'manager_vacant',
        ]
        widgets = {
            'flats': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['new_flat'].widget.attrs.update({'value': ''})
        else:
            self.fields['new_flat'].widget.attrs.update({'value': 'Select Flats'})

    def save(self, commit=True):
        flat_name = self.cleaned_data.get('new_flat')
        if flat_name:
            flat = Flat.objects.create(name=flat_name)
            self.cleaned_data['flats'].add(flat)
        return super(PropertyForm, self).save(commit)

    def clean_new_flat(self):
        flat_name = self.cleaned_data['new_flat']
        if not Flat.objects.filter(name=flat_name).exists():
            return flat_name
        raise forms.ValidationError('Flat with this name already exists.')


User = get_user_model()


class FlatForm(forms.ModelForm):
    #current_tenant = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    #all_tenants = ModelMultipleChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Flat
        fields = [
            'name',
            'number_of_rooms',
            'number_of_living_rooms',
            'number_of_kitchens',
            'number_of_toilets',
            'description',
        ]
    '''def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.template_pack = 'bootstrap5'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))'''

