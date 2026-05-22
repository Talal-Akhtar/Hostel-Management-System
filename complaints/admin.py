"""
complaints/admin.py
===================
Admin registration for Complaint model.
"""

from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'student',
        'category',
        'priority',
        'status',
        'created_at',
        'resolved_at',
    ]

    list_filter   = ['status', 'category', 'priority']
    search_fields = ['title', 'student__roll_number', 'student__user__first_name']
    readonly_fields = ['created_at', 'updated_at', 'resolved_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
