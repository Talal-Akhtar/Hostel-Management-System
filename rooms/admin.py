"""
rooms/admin.py
==============
Registers the Room model with Django Admin.
Includes inline display of assigned students.
"""

from django.contrib import admin
from .models import Room
from students.models import Student


class StudentInline(admin.TabularInline):
    """
    Shows students assigned to a room INSIDE the room's admin page.
    This is an 'inline' — a sub-table inside another model's detail view.
    """
    model = Student
    fields = ['roll_number', 'get_full_name', 'phone_number', 'is_active']
    readonly_fields = ['roll_number', 'get_full_name', 'phone_number']
    extra = 0          # Don't show empty extra rows
    can_delete = False # Prevent accidental deletion from here


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [
        'room_number',
        'floor',
        'room_type',
        'capacity',
        'occupancy_status',
        'monthly_rent',
        'is_active',
    ]

    list_filter   = ['floor', 'room_type', 'is_active']
    search_fields = ['room_number', 'amenities']
    list_per_page = 20

    inlines = [StudentInline]  # Show students inside room detail page
