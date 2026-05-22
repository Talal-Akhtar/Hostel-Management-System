"""
authentication/models.py
========================
We use Django's built-in User model for authentication.
No custom model needed here — the Student model in students/models.py
extends User via OneToOneField.

This file is intentionally minimal.
"""

# No custom models needed.
# Django's built-in User model handles:
#   - username, email, password (hashed)
#   - first_name, last_name
#   - is_active, is_staff, is_superuser
#   - last_login, date_joined
