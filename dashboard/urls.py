"""
dashboard/urls.py
=================
Only one page — the main dashboard overview.
"""

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
]
