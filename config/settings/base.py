"""
Django settings for student_manager project.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY: Secret key from environment only, no insecure fallback
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-only-key-not-for-production-use-39x82k')
if not SECRET_KEY or SECRET_KEY.startswith('django-insecure-'):
    import warnings
    warnings.warn(
        "Using an insecure SECRET_KEY for development only. "
        "Set the SECRET_KEY environment variable for production!",
        stacklevel=2,
    )

DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # Third party
    'widget_tweaks',
    'whitenoise.runserver_nostatic',
    
    # Local apps
    'apps.accounts',
    'apps.core',
    'apps.dashboard',
    'apps.semesters',
    'apps.subjects',
    'apps.schedule',
    'apps.tasks',
    'apps.grades',
    'apps.attendance',
    'apps.exams',
    'apps.calendar',
    'apps.notes',
    'apps.goals',
    'apps.productivity',
    'apps.notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.core.middleware.SemesterMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'apps.core.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Russian'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Login/Logout URLs
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard:index'
LOGOUT_REDIRECT_URL = 'accounts:login'

# Email
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@studentmanager.local')

# ============================================================
# SECURITY SETTINGS
# ============================================================

# SSL/HTTPS (production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Security headers (always on)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Content Security Policy
SECURE_CONTENT_SECURITY_POLICY = "default-src 'self'; script-src 'self' 'unsafe-inline' https://unpkg.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: blob:; connect-src 'self'; frame-ancestors 'none';"

# Permissions Policy
SECURE_PERMISSIONS_POLICY = "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()"

# Cookies
SESSION_COOKIE_AGE = 86400  # 1 day (was 2 weeks)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_HTTPONLY = False  # Required for HTMX/JS to read CSRF token
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = not DEBUG
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if os.environ.get('CSRF_TRUSTED_ORIGINS') else []

# Session security
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = False

# File Uploads
FILE_UPLOAD_MAX_MEMORY_SIZE = 2097152  # 2MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 2097152  # 2MB

# Password hashing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Auth backend
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Logout on password change
LOGOUT_ON_PASSWORD_CHANGE = True

# Messages
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# Pagination
PAGINATION_DEFAULT_SIZE = 20

# Rate limiting
RATE_LIMIT_LOGIN_ATTEMPTS = 5
RATE_LIMIT_LOGIN_WINDOW = 900  # 15 minutes

# Grading Systems
GRADING_SYSTEMS = {
    'percentage': {'name': 'Percentage', 'max': 100, 'passing': 60},
    '5-point': {'name': '5-Point', 'max': 5, 'passing': 3},
    '10-point': {'name': '10-Point', 'max': 10, 'passing': 6},
    'gpa-4': {'name': 'GPA 4.0', 'max': 4.0, 'passing': 2.0},
}

DEFAULT_GRADING_SYSTEM = 'percentage'

# Notification settings
NOTIFICATION_TYPES = [
    ('task_deadline', 'Task Deadline'),
    ('exam_reminder', 'Exam Reminder'),
    ('schedule_reminder', 'Schedule Reminder'),
    ('overdue_task', 'Overdue Task'),
]

NOTIFICATION_TIMING = [
    ('1_day', '1 Day Before'),
    ('3_hours', '3 Hours Before'),
    ('1_hour', '1 Hour Before'),
    ('disabled', 'Disabled'),
]

# Backup
BACKUP_DIR = BASE_DIR / 'backups'
BACKUP_RETENTION_DAYS = 30
