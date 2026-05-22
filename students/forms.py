"""
students/forms.py
=================
Django forms for creating and editing Student records.

Why forms?
  Forms validate user input and convert it to Python objects.
  ModelForm auto-generates fields directly from the model.
"""

from django import forms
from django.contrib.auth.models import User
from .models import Student


class UserForm(forms.ModelForm):
    """
    Form for the built-in User model fields.
    Used alongside StudentForm to create a full student account.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'username':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }


class StudentForm(forms.ModelForm):
    """
    Form for creating or editing a Student profile.
    Excludes 'user' because that's handled by UserForm separately.
    """
    class Meta:
        model = Student
        fields = [
            'roll_number', 'department', 'phone_number',
            'room', 'profile_pic',
            'guardian_name', 'guardian_phone', 'address',
            'is_active',
        ]
        widgets = {
            'roll_number':   forms.TextInput(attrs={'class': 'form-control'}),
            'department':    forms.Select(attrs={'class': 'form-select'}),
            'phone_number':  forms.TextInput(attrs={'class': 'form-control'}),
            'room':          forms.Select(attrs={'class': 'form-select'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_phone':forms.TextInput(attrs={'class': 'form-control'}),
            'address':       forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active':     forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
