"""
complaints/models.py
====================
Tracks student complaints and their resolution status.

Relationships:
  Complaint ──── ForeignKey ──► Student   (one student, many complaints)
"""

from django.db import models
from django.contrib.auth.models import User


class Complaint(models.Model):
    """
    Represents a complaint filed by a student.

    - 'student'        : Who filed the complaint
    - 'title'          : Short heading for the complaint
    - 'complaint_text' : Full description of the issue
    - 'category'       : Type of complaint (maintenance, food, etc.)
    - 'status'         : Current stage (pending → in progress → resolved)
    - 'priority'       : How urgent is this complaint
    - 'admin_response' : Response/note from hostel admin
    - 'resolved_by'    : Which admin resolved it
    - 'resolved_at'    : When it was resolved
    """

    CATEGORY_CHOICES = [
        ('MAINTENANCE', 'Room Maintenance'),
        ('PLUMBING',    'Plumbing'),
        ('ELECTRICAL',  'Electrical'),
        ('FOOD',        'Food / Mess'),
        ('CLEANLINESS', 'Cleanliness'),
        ('SECURITY',    'Security'),
        ('NOISE',       'Noise Complaint'),
        ('INTERNET',    'Internet / WiFi'),
        ('OTHER',       'Other'),
    ]

    STATUS_CHOICES = [
        ('PENDING',     'Pending'),        # Just filed, not seen yet
        ('REVIEWED',    'Under Review'),   # Admin has seen it
        ('IN_PROGRESS', 'In Progress'),    # Being fixed
        ('RESOLVED',    'Resolved'),       # All done
        ('REJECTED',    'Rejected'),       # Not valid / dismissed
    ]

    PRIORITY_CHOICES = [
        ('LOW',    'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH',   'High'),
        ('URGENT', 'Urgent'),
    ]

    # ── Relationships ──────────────────────────────────────────
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='complaints'
    )

    # Admin who resolved the complaint (nullable — may not be resolved yet)
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_complaints'
    )

    # ── Complaint Info ─────────────────────────────────────────
    title          = models.CharField(max_length=200)
    complaint_text = models.TextField(help_text="Describe your issue in detail")
    category       = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default='OTHER')
    priority       = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')

    # ── Status Tracking ────────────────────────────────────────
    status         = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    admin_response = models.TextField(blank=True, help_text="Admin notes or resolution message")
    attachment     = models.ImageField(upload_to='complaints/attachments/', null=True, blank=True)

    # ── Timestamps ─────────────────────────────────────────────
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title} — {self.student}"

    def resolve(self, admin_user, response_text=""):
        """Mark this complaint as resolved."""
        from django.utils import timezone
        self.status = 'RESOLVED'
        self.resolved_by = admin_user
        self.resolved_at = timezone.now()
        if response_text:
            self.admin_response = response_text
        self.save()
