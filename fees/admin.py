"""
fees/admin.py
=============
Admin setup for Fee model with useful list filters and actions.
"""

from django.contrib import admin
from .models import Fee


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = [
        'student',
        'fee_type',
        'month',
        'year',
        'amount',
        'paid_amount',
        'status',
        'due_date',
        'payment_date',
    ]

    list_filter   = ['status', 'fee_type', 'year', 'month']
    search_fields = ['student__roll_number', 'student__user__first_name', 'student__user__last_name']
    list_per_page = 30
    date_hierarchy = 'due_date'   # Adds a date drill-down at the top

    # Custom admin action: mark selected fees as paid
    actions = ['mark_fees_paid']

    def mark_fees_paid(self, request, queryset):
        """Bulk action to mark multiple fees as paid at once."""
        for fee in queryset:
            fee.mark_as_paid()
        self.message_user(request, f"{queryset.count()} fee(s) marked as paid.")
    mark_fees_paid.short_description = "Mark selected fees as Paid"
