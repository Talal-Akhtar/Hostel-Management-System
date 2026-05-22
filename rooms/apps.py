"""
rooms/apps.py
==============
App configuration for the 'rooms' module.
Django reads this to register the app properly.
"""
from django.apps import AppConfig


class RoomsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rooms'
    verbose_name = 'Rooms'
