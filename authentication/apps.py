"""
authentication/apps.py
=======================
App configuration for the 'authentication' module.
Django reads this to register the app properly.
"""
from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
    verbose_name = 'Authentication'
