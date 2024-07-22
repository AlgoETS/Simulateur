"""
Django settings for simulateur project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
from django.core.asgi import get_asgi_application
import django


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-ypedlkwxvkm2gyl%e=joz==zd*2tnfcmqt)tv9zg)j(%4#qq(u")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#CSRF_TRUSTED_ORIGINS = ['*']

# Site and login configurations
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# Application definition
INSTALLED_APPS = [
    'channels',
    'django.contrib.sites',
    'jet',
    'jet.dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_json_widget',
    'simulation',
    'django_check_seo',
    'easyaudit',
    'django_prometheus',
    'tinymce',
    'pictures',
    'imagekit',
    'colorfield',
    'djmoney',
    'any_urlfield',
    'organizations',
    'allauth_ui',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.microsoft',
    'allauth.socialaccount.providers.notion',
    'widget_tweaks',
    'slippers',
    'guest_user',
    'pwa',
    'webpack_loader',
    'sslserver',
    'django_rq',
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.migrations',
    'health_check.contrib.psutil',
    'health_check.contrib.s3boto3_storage',
    'health_check.contrib.rabbitmq',
    'health_check.contrib.redis',
    'storages',
]

# Theme settings
ALLAUTH_UI_THEME = "dark"

# Middleware configuration
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simulation.middleware.CustomXFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

# Webpack loader configuration
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'yourreactapp/',
        'STATS_FILE': os.path.join(BASE_DIR, 'yourreactapp', 'webpack-stats.json'),
    }
}

# URL configuration
ROOT_URLCONF = "simulateur.urls"

# Template settings
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# Database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Channels configuration
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.getenv('REDIS_HOST', 'localhost'), int(os.getenv('REDIS_PORT', 6379)))],
        },
    },
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'uvicorn': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'asgiref': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'simulation': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Authentication settings
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'guest_user.backends.GuestBackend'
)

# Social account providers
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': 'your-google-client-id',
            'secret': 'your-google-client-secret',
            'key': ''
        }
    },
    'github': {
        'APP': {
            'client_id': 'Ov23lieFcjzlTWoPMJC4',
            'secret': 'a0caa32d591edd1e0df91140496c04403796af46',
            'key': ''
        }
    },
    'microsoft': {
        'APP': {
            'client_id': 'your-microsoft-client-id',
            'secret': 'your-microsoft-client-secret',
            'key': ''
        }
    },
    'notion': {
        'APP': {
            'client_id': 'your-not-ion-client-id',
            'secret': '',
            'key': ''
        }
    }
}

# Performance recording
PERF_REC = {
    "MODE": "once",
}

# JET settings
JET_SIDE_MENU_COMPACT = True
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
JET_MODULE_GOOGLE_ANALYTICS_CLIENT_SECRETS_FILE = os.path.join(PROJECT_DIR, 'client_secrets.json')

# PICTURES settings
PICTURES = {
    "BREAKPOINTS": {
        "xs": 576,
        "s": 768,
        "m": 992,
        "l": 1200,
        "xl": 1400,
    },
    "GRID_COLUMNS": 12,
    "CONTAINER_WIDTH": 1200,
    "FILE_TYPES": ["WEBP"],
    "PIXEL_DENSITIES": [1, 2],
    "USE_PLACEHOLDERS": True,
    "QUEUE_NAME": "pictures",
    "PROCESSOR": "pictures.tasks.process_picture",
}

# PWA settings
PWA_APP_NAME = 'Simulateur'
PWA_APP_DESCRIPTION = "Simulateur is a Django web application that helps you simulate your financial decisions."
PWA_APP_THEME_COLOR = '#317EFB'
PWA_APP_BACKGROUND_COLOR = '#FFFFFF'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '/static/images/my_app_icon.png',
        'sizes': '160x160'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/images/my_apple_icon.png',
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/icons/splash-640x1136.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'
PWA_APP_SHORTCUTS = [
    {
        'name': 'Shortcut',
        'url': '/target',
        'description': 'Shortcut to a page in my application'
    }
]
PWA_APP_SCREENSHOTS = [
    {
      'src': '/static/images/icons/splash-750x1334.png',
      'sizes': '750x1334',
      "type": "image/png"
    }
]

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    },
}
# Health check settings
HEALTH_CHECK = {
    'DISK_USAGE_MAX': 90,  # percent
    'MEMORY_MIN': 100,    # in MB
}

# MinIO Storage Configuration
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
AWS_SECRET_ACCESS_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin')
AWS_STORAGE_BUCKET_NAME = 'mybucket'  # Replace with your bucket name
AWS_S3_ENDPOINT_URL = os.getenv('MINIO_URL', 'http://localhost:9000')
AWS_S3_CUSTOM_DOMAIN = None
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = False

# InfluxDB settings
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "my-token")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "my-org")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "my-bucket")

CACHE_TTL = 30

# ASGI and WSGI application settings
ASGI_APPLICATION = 'simulateur.asgi.application'
# WSGI_APPLICATION = 'simulateur.wsgi.application'
