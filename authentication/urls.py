"""
authentication/urls.py
======================
URL patterns for login, logout, and registration.

All these URLs are prefixed with /auth/ (from root urls.py)
So the actual URLs are:
  /auth/login/
  /auth/logout/
  /auth/register/
  /auth/profile/
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'auth'

urlpatterns = [
    # ── Login / Logout ─────────────────────────────────────────
    # Django provides built-in views for login/logout
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='authentication/login.html'),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # ── Custom Views ───────────────────────────────────────────
    path('register/', views.register_view, name='register'),
    path('profile/',  views.profile_view,  name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
]
