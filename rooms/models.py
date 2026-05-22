"""
rooms/models.py
===============
Defines the Room model for hostel room management.

Relationships:
  Room ◄──── ForeignKey ──── Student   (many students can be in one room)

Note:
  We DON'T store students directly here.
  Instead, the Student model has a ForeignKey pointing to Room.
  Django lets us access all students in a room via: room.students.all()
"""

from django.db import models


class Room(models.Model):
    """
    Represents a physical room in the hostel.

    - 'room_number'  : Unique identifier (e.g. "101", "B-204")
    - 'floor'        : Which floor the room is on
    - 'room_type'    : Single, Double, Triple, Dormitory
    - 'capacity'     : Max students allowed
    - 'monthly_rent' : Rent charged per month
    - 'amenities'    : Short description of what's included
    - 'is_available' : Computed from capacity vs current students
    """

    ROOM_TYPE_CHOICES = [
        ('SINGLE', 'Single Occupancy'),
        ('DOUBLE', 'Double Occupancy'),
        ('TRIPLE', 'Triple Occupancy'),
        ('DORM',   'Dormitory (4+)'),
    ]

    FLOOR_CHOICES = [
        (0, 'Ground Floor'),
        (1, 'First Floor'),
        (2, 'Second Floor'),
        (3, 'Third Floor'),
        (4, 'Fourth Floor'),
    ]

    room_number  = models.CharField(max_length=10, unique=True, help_text="e.g. 101 or B-204")
    floor        = models.IntegerField(choices=FLOOR_CHOICES, default=0)
    room_type    = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES, default='DOUBLE')
    capacity     = models.PositiveIntegerField(default=2, help_text="Maximum number of students")
    monthly_rent = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    amenities    = models.TextField(blank=True, help_text="e.g. WiFi, AC, Attached Bath")
    is_active    = models.BooleanField(default=True, help_text="Is this room currently usable?")
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['room_number']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return f"Room {self.room_number} ({self.get_room_type_display()})"

    def get_current_occupancy(self):
        """Returns the number of students currently assigned to this room."""
        return self.students.filter(is_active=True).count()

    def get_available_beds(self):
        """Returns how many beds are still free."""
        return self.capacity - self.get_current_occupancy()

    def is_full(self):
        """Returns True if room has no free beds."""
        return self.get_available_beds() <= 0

    def occupancy_status(self):
        """Returns a human-readable occupancy status."""
        occ = self.get_current_occupancy()
        return f"{occ}/{self.capacity}"
