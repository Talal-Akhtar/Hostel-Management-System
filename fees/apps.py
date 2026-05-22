"""
fees/apps.py
=============
App configuration for the 'fees' module.
Django reads this to register the app properly.
"""
from django.apps import AppConfig


class FeesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fees'
    verbose_name = 'Fees'
