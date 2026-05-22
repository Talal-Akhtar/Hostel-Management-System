"""
visitors/urls.py
====================
URL patterns for the visitors module.
All URLs here are prefixed with /visitors/ (from root urls.py).
"""

from django.urls import path
from . import views

app_name = 'visitors'

urlpatterns = [
    path('',          views.index,  name='index'),   # List all visitors
    path('<int:pk>/', views.detail, name='detail'),  # View single record
    path('add/',      views.add,    name='add'),      # Create new
    path('<int:pk>/edit/',   views.edit,   name='edit'),    # Update
    path('<int:pk>/delete/', views.delete, name='delete'),  # Delete
]
