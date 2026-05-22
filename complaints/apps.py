"""
complaints/apps.py
===================
App configuration for the 'complaints' module.
Django reads this to register the app properly.
"""
from django.apps import AppConfig


class ComplaintsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'complaints'
    verbose_name = 'Complaints'
