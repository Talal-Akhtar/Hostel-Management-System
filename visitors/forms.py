"""
visitors/forms.py
=================
Form for logging a new visitor entry.
"""

from django import forms
from .models import Visitor


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = [
            'student', 'visitor_name', 'visitor_phone', 'relation',
            'purpose', 'id_proof_type', 'id_proof_number',
            'entry_time', 'exit_time', 'approved_by', 'notes',
        ]
        widgets = {
            'student':        forms.Select(attrs={'class': 'form-select'}),
            'visitor_name':   forms.TextInput(attrs={'class': 'form-control'}),
            'visitor_phone':  forms.TextInput(attrs={'class': 'form-control'}),
            'relation':       forms.Select(attrs={'class': 'form-select'}),
            'purpose':        forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'id_proof_type':  forms.Select(attrs={'class': 'form-select'}),
            'id_proof_number':forms.TextInput(attrs={'class': 'form-control'}),
            'entry_time':     forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'exit_time':      forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'approved_by':    forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Guard/Admin name'}),
            'notes':          forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
