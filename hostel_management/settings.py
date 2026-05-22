"""
Django Settings for Hostel Management System
=============================================
This file controls all core configurations for the project.
"""

import os
from pathlib import Path

# ─────────────────────────────────────────────────────────
# BASE DIRECTORY
# Path(__file__) = this file (settings.py)
# .resolve().parent.parent = two levels up = project root
# ─────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────────────────
# SECURITY
# NEVER expose SECRET_KEY in production — use env variables
# ─────────────────────────────────────────────────────────
SECRET_KEY = 'django-insecure-hostel-mgmt-secret-key-change-in-production'

# Set to False in production
DEBUG = True

# In production: ['yourdomain.com', 'www.yourdomain.com']
ALLOWED_HOSTS = ['*']


# ─────────────────────────────────────────────────────────
# INSTALLED APPS
# Django built-ins first, then third-party, then our apps
# ─────────────────────────────────────────────────────────
INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Our custom apps (each is a module of the system)
    'authentication',   # Login, logout, user registration
    'students',         # Student profiles and info
    'rooms',            # Room allocation and management
    'fees',             # Fee records and payments
    'complaints',       # Student complaint tracking
    'visitors',         # Visitor entry/exit log
    'dashboard',        # Summary stats and overview
]

# ─────────────────────────────────────────────────────────
# MIDDLEWARE
# These run on every request/response (security, sessions, auth)
# ─────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ─────────────────────────────────────────────────────────
# URL CONFIGURATION
# Django will look in hostel_management/urls.py first
# ─────────────────────────────────────────────────────────
ROOT_URLCONF = 'hostel_management.urls'

# ─────────────────────────────────────────────────────────
# TEMPLATES
# Django uses these settings to find and render HTML files
# ─────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Look in a shared 'templates/' folder at project root
        'DIRS': [BASE_DIR / 'templates'],
        # Also look in each app's own templates/ subfolder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ─────────────────────────────────────────────────────────
# WSGI
# Entry point for production web servers (Gunicorn, uWSGI)
# ─────────────────────────────────────────────────────────
WSGI_APPLICATION = 'hostel_management.wsgi.application'


# ─────────────────────────────────────────────────────────
# DATABASE
# SQLite is the default — no extra setup needed
# In production, switch to PostgreSQL or MySQL
# ─────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ─────────────────────────────────────────────────────────
# PASSWORD VALIDATION
# Django will reject weak passwords using these validators
# ─────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ─────────────────────────────────────────────────────────
# INTERNATIONALIZATION
# Time zone set to Pakistan — change as needed
# ─────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_TZ = True


# ─────────────────────────────────────────────────────────
# STATIC FILES (CSS, JavaScript, Images)
# STATIC_URL  = URL prefix when browsers request static files
# STATICFILES_DIRS = where Django looks for static files in dev
# STATIC_ROOT = where 'collectstatic' gathers files for prod
# ─────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'


# ─────────────────────────────────────────────────────────
# MEDIA FILES (User-uploaded content, e.g., profile pictures)
# MEDIA_URL  = URL prefix for uploaded files
# MEDIA_ROOT = folder on disk where uploads are stored
# ─────────────────────────────────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ─────────────────────────────────────────────────────────
# LOGIN / LOGOUT REDIRECTS
# After login  → go to dashboard
# After logout → go to login page
# ─────────────────────────────────────────────────────────
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/auth/login/'


# ─────────────────────────────────────────────────────────
# DEFAULT PRIMARY KEY TYPE
# All models use BigAutoField (64-bit integer) as default PK
# ─────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
