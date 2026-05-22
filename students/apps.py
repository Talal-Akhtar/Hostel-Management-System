"""
students/apps.py
=================
App configuration for the 'students' module.
Django reads this to register the app properly.
"""
from django.apps import AppConfig


class StudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'students'
    verbose_name = 'Students'
