"""
visitors/models.py
==================
Tracks visitors entering the hostel to visit a student.

Relationships:
  Visitor ──── ForeignKey ──► Student   (one student can have many visitors)
"""

from django.db import models
from django.utils import timezone


class Visitor(models.Model):
    """
    Logs a visitor's entry to the hostel.

    - 'student'       : Which student the visitor is meeting
    - 'visitor_name'  : Full name of the visitor
    - 'visitor_phone' : Visitor's contact number
    - 'relation'      : How the visitor is related to the student
    - 'purpose'       : Reason for visit
    - 'entry_time'    : When they entered the hostel
    - 'exit_time'     : When they left (null if still inside)
    - 'id_proof_type' : Type of ID they showed (CNIC, Passport, etc.)
    - 'id_proof_number': The actual ID number
    - 'approved_by'   : Guard/admin who let them in
    """

    RELATION_CHOICES = [
        ('PARENT',   'Parent'),
        ('SIBLING',  'Brother/Sister'),
        ('RELATIVE', 'Relative'),
        ('FRIEND',   'Friend'),
        ('OTHER',    'Other'),
    ]

    ID_PROOF_CHOICES = [
        ('CNIC',       'CNIC / National ID'),
        ('PASSPORT',   'Passport'),
        ('DRIVING',    'Driving License'),
        ('STUDENT_ID', 'Student ID'),
        ('OTHER',      'Other'),
    ]

    # ── Relationship ───────────────────────────────────────────
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='visitors',
        help_text="The student being visited"
    )

    # ── Visitor Details ────────────────────────────────────────
    visitor_name   = models.CharField(max_length=100)
    visitor_phone  = models.CharField(max_length=15, blank=True)
    relation       = models.CharField(max_length=10, choices=RELATION_CHOICES, default='OTHER')
    purpose        = models.TextField(blank=True, help_text="Reason for visiting")

    # ── ID Verification ────────────────────────────────────────
    id_proof_type   = models.CharField(max_length=15, choices=ID_PROOF_CHOICES, default='CNIC')
    id_proof_number = models.CharField(max_length=50, blank=True)

    # ── Timing ─────────────────────────────────────────────────
    # default=timezone.now means time is auto-set when record is created
    entry_time = models.DateTimeField(default=timezone.now)
    exit_time  = models.DateTimeField(null=True, blank=True, help_text="Leave blank if still inside")

    # ── Admin ──────────────────────────────────────────────────
    approved_by = models.CharField(max_length=100, blank=True, help_text="Guard or admin name")
    notes       = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-entry_time']
        verbose_name = 'Visitor'
        verbose_name_plural = 'Visitors'

    def __str__(self):
        return f"{self.visitor_name} visiting {self.student} on {self.entry_time.strftime('%d %b %Y')}"

    def is_inside(self):
        """Returns True if visitor has entered but not yet exited."""
        return self.exit_time is None

    def duration(self):
        """Returns visit duration if visitor has left."""
        if self.exit_time:
            diff = self.exit_time - self.entry_time
            hours, remainder = divmod(diff.seconds, 3600)
            minutes = remainder // 60
            return f"{hours}h {minutes}m"
        return "Still Inside"

    def record_exit(self):
        """Mark the visitor as exited."""
        self.exit_time = timezone.now()
        self.save()
