"""
fees/models.py
==============
Manages hostel fee records for students.

Relationships:
  Fee ──── ForeignKey ──► Student   (one student can have many fee records)

Each row in this table = one fee invoice (monthly or yearly).
"""

from django.db import models
from django.utils import timezone


class Fee(models.Model):
    """
    Represents a single fee record for a student.

    - 'student'      : Which student this fee belongs to
    - 'amount'       : Total amount due
    - 'paid_amount'  : How much has been paid so far
    - 'is_paid'      : True when fully paid
    - 'due_date'     : Deadline for payment
    - 'payment_date' : When payment was actually received
    - 'month'        : Which month this fee is for
    - 'fee_type'     : Room rent, food, electricity, etc.
    - 'remarks'      : Any notes (e.g. "Late fee applied")
    """

    FEE_TYPE_CHOICES = [
        ('ROOM',    'Room Rent'),
        ('FOOD',    'Food / Mess'),
        ('ELEC',    'Electricity'),
        ('WATER',   'Water'),
        ('LAUNDRY', 'Laundry'),
        ('OTHER',   'Other'),
    ]

    STATUS_CHOICES = [
        ('PENDING',   'Pending'),
        ('PARTIAL',   'Partially Paid'),
        ('PAID',      'Fully Paid'),
        ('OVERDUE',   'Overdue'),
        ('WAIVED',    'Waived'),
    ]

    MONTH_CHOICES = [
        (1, 'January'),   (2, 'February'),  (3, 'March'),
        (4, 'April'),     (5, 'May'),       (6, 'June'),
        (7, 'July'),      (8, 'August'),    (9, 'September'),
        (10, 'October'), (11, 'November'), (12, 'December'),
    ]

    # ── Relationships ──────────────────────────────────────────
    # on_delete=CASCADE: if student is deleted, delete their fees too
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='fees',
        help_text="The student this fee is charged to"
    )

    # ── Fee Details ────────────────────────────────────────────
    fee_type    = models.CharField(max_length=10, choices=FEE_TYPE_CHOICES, default='ROOM')
    amount      = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total amount due")
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    # ── Time Fields ────────────────────────────────────────────
    month        = models.PositiveIntegerField(choices=MONTH_CHOICES, default=1)
    year         = models.PositiveIntegerField(default=2025)
    due_date     = models.DateField(help_text="Payment deadline")
    payment_date = models.DateField(null=True, blank=True, help_text="Date payment was received")
    created_at   = models.DateTimeField(auto_now_add=True)

    # ── Notes ──────────────────────────────────────────────────
    remarks = models.TextField(blank=True, help_text="Optional notes about this fee record")

    class Meta:
        ordering = ['-year', '-month']
        verbose_name = 'Fee Record'
        verbose_name_plural = 'Fee Records'
        # Prevent duplicate fee entries for same student/type/month/year
        unique_together = ['student', 'fee_type', 'month', 'year']

    def __str__(self):
        return f"{self.student} — {self.get_fee_type_display()} ({self.get_month_display()} {self.year})"

    def remaining_amount(self):
        """How much is still owed."""
        return self.amount - self.paid_amount

    def mark_as_paid(self):
        """Mark this fee as fully paid."""
        self.paid_amount = self.amount
        self.status = 'PAID'
        self.payment_date = timezone.now().date()
        self.save()

    def is_overdue(self):
        """Check if due date has passed and fee is not paid."""
        from datetime import date
        return self.status not in ('PAID', 'WAIVED') and date.today() > self.due_date
