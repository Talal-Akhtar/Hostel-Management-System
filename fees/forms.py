"""
fees/forms.py
=============
Form for creating and editing Fee records.
"""

from django import forms
from .models import Fee


class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = [
            'student', 'fee_type', 'amount', 'paid_amount',
            'status', 'month', 'year', 'due_date', 'payment_date', 'remarks',
        ]
        widgets = {
            'student':      forms.Select(attrs={'class': 'form-select'}),
            'fee_type':     forms.Select(attrs={'class': 'form-select'}),
            'amount':       forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'paid_amount':  forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status':       forms.Select(attrs={'class': 'form-select'}),
            'month':        forms.Select(attrs={'class': 'form-select'}),
            'year':         forms.NumberInput(attrs={'class': 'form-control', 'min': 2020, 'max': 2100}),
            'due_date':     forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'remarks':      forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
