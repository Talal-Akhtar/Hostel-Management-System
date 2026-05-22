"""
dashboard/views.py
==================
The dashboard aggregates summary statistics from all other modules.
This is the home page after login.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    """
    Main dashboard: pulls counts and summaries from all modules.
    We use lazy imports to avoid circular import issues.
    """
    from students.models   import Student
    from rooms.models      import Room
    from fees.models       import Fee
    from complaints.models import Complaint
    from visitors.models   import Visitor

    context = {
        # ── Student Stats ──────────────────────────────────
        'total_students'  : Student.objects.filter(is_active=True).count(),
        'inactive_students': Student.objects.filter(is_active=False).count(),

        # ── Room Stats ─────────────────────────────────────
        'total_rooms'     : Room.objects.filter(is_active=True).count(),
        'full_rooms'      : sum(1 for r in Room.objects.all() if r.is_full()),

        # ── Fee Stats ──────────────────────────────────────
        'pending_fees'    : Fee.objects.filter(status='PENDING').count(),
        'overdue_fees'    : Fee.objects.filter(status='OVERDUE').count(),
        'paid_fees_today' : Fee.objects.filter(status='PAID').count(),

        # ── Complaint Stats ────────────────────────────────
        'open_complaints' : Complaint.objects.filter(status__in=['PENDING', 'REVIEWED', 'IN_PROGRESS']).count(),
        'resolved_complaints': Complaint.objects.filter(status='RESOLVED').count(),

        # ── Visitor Stats ──────────────────────────────────
        'visitors_inside' : Visitor.objects.filter(exit_time__isnull=True).count(),

        # ── Recent Activity ────────────────────────────────
        'recent_complaints': Complaint.objects.select_related('student__user').order_by('-created_at')[:5],
        'recent_visitors'  : Visitor.objects.select_related('student__user').order_by('-entry_time')[:5],
        'recent_fees'      : Fee.objects.select_related('student__user').order_by('-created_at')[:5],
    }

    return render(request, 'dashboard/index.html', context)
