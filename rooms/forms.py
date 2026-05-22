"""
rooms/forms.py
==============
Form for creating and editing Room records.
"""

from django import forms
from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'room_number', 'floor', 'room_type',
            'capacity', 'monthly_rent', 'amenities', 'is_active',
        ]
        widgets = {
            'room_number':  forms.TextInput(attrs={'class': 'form-control'}),
            'floor':        forms.Select(attrs={'class': 'form-select'}),
            'room_type':    forms.Select(attrs={'class': 'form-select'}),
            'capacity':     forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 20}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'amenities':    forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                  'placeholder': 'e.g. WiFi, AC, Attached Bathroom'}),
            'is_active':    forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
