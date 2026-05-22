"""
authentication/views.py
=======================
Handles user registration, profile view, and password change.
Login/Logout are handled by Django's built-in auth views.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register_view(request):
    """
    Allow new users to create an account.
    Uses Django's built-in UserCreationForm (username + password).
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)            # Log them in automatically after registration
            messages.success(request, f"Account created! Welcome, {user.username}.")
            return redirect('dashboard:index')
    else:
        form = UserCreationForm()

    return render(request, 'authentication/register.html', {'form': form})


@login_required
def profile_view(request):
    """
    Show the currently logged-in user's profile.
    @login_required: redirects to /auth/login/ if not logged in.
    """
    return render(request, 'authentication/profile.html', {'user': request.user})


@login_required
def change_password_view(request):
    """Allow logged-in users to change their password."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update session so user isn't logged out after password change
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect('auth:profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'authentication/change_password.html', {'form': form})
