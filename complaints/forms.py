"""
complaints/forms.py
===================
Form for students to file a complaint and for admins to respond.
"""

from django import forms
from .models import Complaint


class ComplaintForm(forms.ModelForm):
    """Used by students to file a new complaint."""
    class Meta:
        model = Complaint
        fields = ['student', 'title', 'complaint_text', 'category', 'priority', 'attachment']
        widgets = {
            'student':        forms.Select(attrs={'class': 'form-select'}),
            'title':          forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Brief title of your complaint'}),
            'complaint_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                                                    'placeholder': 'Describe the issue in detail...'}),
            'category':       forms.Select(attrs={'class': 'form-select'}),
            'priority':       forms.Select(attrs={'class': 'form-select'}),
        }


class ComplaintResponseForm(forms.ModelForm):
    """Used by admins to update status and add a response."""
    class Meta:
        model = Complaint
        fields = ['status', 'admin_response']
        widgets = {
            'status':         forms.Select(attrs={'class': 'form-select'}),
            'admin_response': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                                    'placeholder': 'Write your response or resolution note...'}),
        }
