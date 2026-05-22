"""
students/models.py
==================
Defines the Student model — the CORE entity of this system.
Every other module (fees, complaints, visitors, rooms) links to a Student.

Relationship:
  Student ──── OneToOne ────► User   (Django's built-in User model)
  Student ──── ForeignKey ──► Room   (one room can have many students)
"""

from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    """
    Stores hostel student profile information.

    - 'user'        : Links to Django's built-in User (provides login, password, email)
    - 'roll_number' : Unique college/university ID
    - 'department'  : Student's academic department
    - 'phone_number': Contact number
    - 'room'        : Which room they're assigned to (can be empty)
    - 'profile_pic' : Optional photo upload
    - 'date_joined' : When the student record was created
    - 'is_active'   : Whether the student is currently staying

    Why OneToOne with User?
      Each student is ALSO a user who can log in.
      OneToOne means one User = one Student (not two students sharing a login).
    """

    DEPARTMENT_CHOICES = [
        ('CS',   'Computer Science'),
        ('EE',   'Electrical Engineering'),
        ('ME',   'Mechanical Engineering'),
        ('CE',   'Civil Engineering'),
        ('BBA',  'Business Administration'),
        ('MED',  'Medical'),
        ('LAW',  'Law'),
        ('OTHER','Other'),
    ]

    # ── Core Fields ───────────────────────────────────────────────
    # on_delete=CASCADE: if the User is deleted, delete this student too
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        help_text="The login account linked to this student"
    )

    roll_number = models.CharField(
        max_length=20,
        unique=True,
        help_text="e.g. CS-2021-001"
    )

    department = models.CharField(
        max_length=10,
        choices=DEPARTMENT_CHOICES,
        default='CS'
    )

    phone_number = models.CharField(
        max_length=15,
        help_text="e.g. +92-300-1234567"
    )

    # ── Room Assignment ───────────────────────────────────────────
    # null=True: Student may not be assigned a room yet
    # on_delete=SET_NULL: if the room is deleted, don't delete student
    room = models.ForeignKey(
        'rooms.Room',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        help_text="The room this student is allocated to"
    )

    # ── Extra Info ────────────────────────────────────────────────
    profile_pic = models.ImageField(
        upload_to='students/profile_pics/',
        null=True,
        blank=True
    )

    # Parent/guardian contact
    guardian_name  = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=15,  blank=True)

    address = models.TextField(blank=True, help_text="Permanent home address")

    date_joined = models.DateField(auto_now_add=True)
    is_active   = models.BooleanField(default=True, help_text="Currently residing?")

    class Meta:
        ordering = ['roll_number']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"

    def get_full_name(self):
        return self.user.get_full_name()

    def get_email(self):
        return self.user.email
