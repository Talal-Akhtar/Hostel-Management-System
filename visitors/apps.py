"""
visitors/apps.py
=================
App configuration for the 'visitors' module.
Django reads this to register the app properly.
"""
from django.apps import AppConfig


class VisitorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'visitors'
    verbose_name = 'Visitors'
