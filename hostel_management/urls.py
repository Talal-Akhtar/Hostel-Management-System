"""
ROOT URL CONFIGURATION — hostel_management/urls.py
====================================================
This is the MAIN URL file. Django checks this first for every request.
Each app has its own urls.py — we include them here using include().

URL Pattern:
  /          → redirect to dashboard
  /auth/     → authentication (login, logout, register)
  /students/ → student management
  /rooms/    → room allocation
  /fees/     → fee management
  /complaints/ → complaint system
  /visitors/ → visitor management
  /dashboard/ → dashboard overview
  /admin/    → Django admin panel
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    # ── Django Admin ──────────────────────────────────────────
    # Built-in admin panel — access at /admin/
    path('admin/', admin.site.urls),

    # ── Root redirect ─────────────────────────────────────────
    # Visiting "/" will redirect to the dashboard
    path('', lambda request: redirect('dashboard:index'), name='home'),

    # ── Authentication ────────────────────────────────────────
    # Handles login, logout, register
    path('auth/', include('authentication.urls', namespace='auth')),

    # ── Core Modules ──────────────────────────────────────────
    path('students/',   include('students.urls',   namespace='students')),
    path('rooms/',      include('rooms.urls',      namespace='rooms')),
    path('fees/',       include('fees.urls',       namespace='fees')),
    path('complaints/', include('complaints.urls', namespace='complaints')),
    path('visitors/',   include('visitors.urls',   namespace='visitors')),
    path('dashboard/',  include('dashboard.urls',  namespace='dashboard')),
]

# ── Serve uploaded media files during development ─────────────
# In production, let Nginx/Apache serve /media/ files instead
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
