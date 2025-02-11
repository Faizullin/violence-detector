from django import forms

from .models import Device


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'description', 'lang', 'lat']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Название',
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Описание',
        })
        self.fields['lang'].widget.attrs.update({
            'class': 'form-control position-lang-field',
            'placeholder': 'Долгота',
        })
        self.fields['lat'].widget.attrs.update({
            'class': 'form-control position-lat-field',
            'placeholder': 'Широта',
        })
