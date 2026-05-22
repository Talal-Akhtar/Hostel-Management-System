"""
rooms/urls.py
=================
URL patterns for the rooms module.
All URLs here are prefixed with /rooms/ (from root urls.py).
"""

from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('',          views.index,  name='index'),   # List all rooms
    path('<int:pk>/', views.detail, name='detail'),  # View single record
    path('add/',      views.add,    name='add'),      # Create new
    path('<int:pk>/edit/',   views.edit,   name='edit'),    # Update
    path('<int:pk>/delete/', views.delete, name='delete'),  # Delete
]
