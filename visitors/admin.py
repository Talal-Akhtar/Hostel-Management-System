"""
visitors/admin.py
=================
Admin registration for Visitor model.
"""

from django.contrib import admin
from .models import Visitor


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = [
        'visitor_name',
        'student',
        'relation',
        'entry_time',
        'exit_time',
        'is_inside',
        'approved_by',
    ]

    list_filter   = ['relation', 'id_proof_type']
    search_fields = ['visitor_name', 'student__roll_number', 'student__user__first_name']
    readonly_fields = ['created_at', 'duration']
    list_per_page = 30
    date_hierarchy = 'entry_time'
