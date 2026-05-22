"""
dashboard/apps.py
==================
App configuration for the 'dashboard' module.
Django reads this to register the app properly.
"""
from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'
    verbose_name = 'Dashboard'
