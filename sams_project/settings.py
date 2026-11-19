"""
Django settings for sams_project project.
Student Assignment Management System (SAMS)
Production & Deployment Ready
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import pymysql
import dj_database_url

pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env
load_dotenv(BASE_DIR / '.env')

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-sams-gtu-bca-sem5-minor-project-key-2026')

DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')

# Host configuration
allowed_hosts_raw = os.getenv('ALLOWED_HOSTS', '*')
if allowed_hosts_raw.strip() == '*':
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_raw.split(',') if h.strip()]

# CSRF Trusted Origins for cloud deployments (Render, Railway, PythonAnywhere, custom domains)
csrf_origins_raw = os.getenv('CSRF_TRUSTED_ORIGINS', '')
if csrf_origins_raw:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in csrf_origins_raw.split(',') if o.strip()]
else:
    CSRF_TRUSTED_ORIGINS = [
        'http://127.0.0.1',
        'http://localhost',
        'https://*.onrender.com',
        'https://*.railway.app',
        'https://*.pythonanywhere.com',
        'https://*.vercel.app',
    ]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'sams_app.apps.SamsAppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sams_project.urls'

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
                'sams_app.context_processors.sams_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'sams_project.wsgi.application'

# Database Configuration
# Priority:
# 1. DATABASE_URL environment variable (Render, Railway, Heroku, Supabase, Neon)
# 2. Local/Remote MySQL via DB_* environment variables
# 3. Automatic fallback to SQLite (db.sqlite3)

database_url = os.getenv('DATABASE_URL')
if database_url:
    DATABASES = {
        'default': dj_database_url.config(
            default=database_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    db_engine = os.getenv('DB_ENGINE', 'django.db.backends.mysql')
    db_name = os.getenv('DB_NAME', 'sams_db')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_host = os.getenv('DB_HOST', '127.0.0.1')
    db_port = os.getenv('DB_PORT', '3306')

    use_mysql = False
    if 'mysql' in db_engine:
        try:
            test_conn = pymysql.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                port=int(db_port),
                connect_timeout=2
            )
            with test_conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            test_conn.close()
            use_mysql = True
        except Exception as e:
            print(f"[SAMS NOTICE] MySQL connection attempt returned: {e}. Falling back to SQLite backend.")
            use_mysql = False

    if use_mysql:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': db_name,
                'USER': db_user,
                'PASSWORD': db_password,
                'HOST': db_host,
                'PORT': db_port,
                'OPTIONS': {
                    'charset': 'utf8mb4',
                    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                }
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 4},
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images) with WhiteNoise production compression
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Media files (Submissions, attachments)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File upload limits (10 MB max)
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB in bytes
ALLOWED_UPLOAD_EXTENSIONS = ['pdf', 'doc', 'docx', 'zip', 'jpg', 'png']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/login-redirect/'
LOGOUT_REDIRECT_URL = '/'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Production Security Headers (when DEBUG=False)
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    # Optional SSL redirect toggle from environment
    if os.getenv('SECURE_SSL_REDIRECT', 'False').lower() in ('true', '1'):
        SECURE_SSL_REDIRECT = True
        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SECURE = True
