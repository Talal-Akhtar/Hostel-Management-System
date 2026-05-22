"""
students/admin.py
=================
Registers the Student model with Django Admin.
This makes it appear at /admin/ so you can manage students via a GUI.
"""

from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Customizes how the Student model looks in the admin panel.

    list_display   : columns shown in the table view
    list_filter    : filter sidebar on the right
    search_fields  : which fields the search box searches
    list_per_page  : pagination
    readonly_fields: fields shown but not editable
    """

    list_display = [
        'roll_number',
        'get_full_name',
        'department',
        'phone_number',
        'room',
        'is_active',
        'date_joined',
    ]

    list_filter   = ['department', 'is_active', 'room__floor']
    search_fields = ['roll_number', 'user__first_name', 'user__last_name', 'user__email', 'phone_number']
    list_per_page = 25
    readonly_fields = ['date_joined']

    # Organize the detail/edit page into sections
    fieldsets = (
        ('Account', {
            'fields': ('user',)
        }),
        ('Student Info', {
            'fields': ('roll_number', 'department', 'phone_number', 'profile_pic')
        }),
        ('Room Assignment', {
            'fields': ('room',)
        }),
        ('Guardian / Contact', {
            'fields': ('guardian_name', 'guardian_phone', 'address'),
            'classes': ('collapse',)   # This section starts collapsed
        }),
        ('Status', {
            'fields': ('is_active', 'date_joined')
        }),
    )
