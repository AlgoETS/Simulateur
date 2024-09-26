import os
from pathlib import Path
from decouple import config

# General settings
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = config("DJANGO_SECRET_KEY", default="django-insecure-default-secret-key")
DEBUG = config("DEBUG", cast=bool, default=False)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost").split(",")

# Site and login configurations
SITE_ID = config("SITE_ID", cast=int, default=1)
LOGIN_REDIRECT_URL = config("LOGIN_REDIRECT_URL", default='/')
ACCOUNT_LOGOUT_REDIRECT_URL = config("ACCOUNT_LOGOUT_REDIRECT_URL", default='/')

# Application definition
INSTALLED_APPS = [
    'channels',
    'django.contrib.sites',

    # Admin
    'jet',
    'jet.dashboard',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    # SEO
    'django_check_seo',
    'easyaudit',

    # Monitoring
    'django_prometheus',

    # Field types
    'pictures',
    'imagekit',
    'colorfield',
    'djmoney',
    'any_urlfield',
    'tinymce',

    # Authentication
    'organizations',
    'guest_user',

    # Allauth
    'allauth_ui',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.microsoft',
    'allauth.socialaccount.providers.notion',

    # UI
    'widget_tweaks',
    'slippers',

    # Web app
    'pwa',

    # SSL Server
    'sslserver',

    # Django channels
    'django_rq',

    # Health check
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.migrations',
    'health_check.contrib.psutil',
    'health_check.contrib.s3boto3_storage',
    'health_check.contrib.rabbitmq',
    'health_check.contrib.redis',

    # Storage
    'storages',

    # Celery
    'django_celery_beat',
    'django_celery_results',

    # Swagger
    'drf_yasg',

    # Local apps
    'simulation',
    'backtesting',
]

# Middleware
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

ROOT_URLCONF = "simulateur.urls"

# Templates
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
DATABASE_ENGINE = config("DATABASE_ENGINE", default="sqlite")

if DATABASE_ENGINE == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("POSTGRES_DB", default="postgres"),
            "USER": config("POSTGRES_USER", default="postgres"),
            "PASSWORD": config("POSTGRES_PASSWORD", default="postgres"),
            "HOST": config("POSTGRES_HOST", default="db"),
            "PORT": config("POSTGRES_PORT", default="5432"),
        }
    }
else:  # Default to sqlite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
            'OPTIONS': {
                'timeout': 20,
            }
        }
    }

# Static and media files configuration
STATIC_URL = config("STATIC_URL", default='/static/')
STATIC_ROOT = config("STATIC_ROOT", default=os.path.join(BASE_DIR, 'staticfiles'))
STATICFILES_STORAGE = config("STATICFILES_STORAGE", default='whitenoise.storage.CompressedManifestStaticFilesStorage')

MEDIA_URL = config("MEDIA_URL", default='/media/')
MEDIA_ROOT = config("MEDIA_ROOT", default=os.path.join(BASE_DIR, 'media'))

# File Storage (MinIO)
DEFAULT_FILE_STORAGE = config("DEFAULT_FILE_STORAGE", default='storages.backends.s3boto3.S3Boto3Storage')
MINIO_STORAGE_ENDPOINT = config("MINIO_STORAGE_ENDPOINT", default='http://minio:9000')
MINIO_STORAGE_ACCESS_KEY = config("MINIO_STORAGE_ACCESS_KEY", default='minioadmin')
MINIO_STORAGE_SECRET_KEY = config("MINIO_STORAGE_SECRET_KEY", default='minioadmin')
MINIO_STORAGE_USE_HTTPS = config("MINIO_STORAGE_USE_HTTPS", cast=bool, default=False)
MINIO_STORAGE_MEDIA_BUCKET_NAME = config("MINIO_STORAGE_MEDIA_BUCKET_NAME", default='media')
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = config("MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET", cast=bool, default=True)
MINIO_STORAGE_STATIC_BUCKET_NAME = config("MINIO_STORAGE_STATIC_BUCKET_NAME", default='static')
MINIO_STORAGE_MEDIA_OBJECT_METADATA = {"Cache-Control": "max-age=1000"}
AWS_ACCESS_KEY_ID = config('MINIO_ACCESS_KEY', default='minioadmin')
AWS_SECRET_ACCESS_KEY = config('MINIO_SECRET_KEY', default='minioadmin')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='media')
AWS_S3_ENDPOINT_URL = config('MINIO_URL', default='http://minio:9000')
AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN', default=None)
AWS_S3_FILE_OVERWRITE = config('AWS_S3_FILE_OVERWRITE', cast=bool, default=False)
AWS_DEFAULT_ACL = config('AWS_DEFAULT_ACL', default=None)
AWS_S3_VERIFY = config('AWS_S3_VERIFY', cast=bool, default=False)

# Celery configuration
CELERY_BROKER_URL = config('CELERY_BROKER_REDIS_URL', default='redis://redis:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='django-db')
CELERY_BEAT_SCHEDULER = config('CELERY_BEAT_SCHEDULER', default='django_celery_beat.schedulers.DatabaseScheduler')


# Channels configuration
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": config("CHANNEL_BACKEND", default="channels_redis.pubsub.RedisPubSubChannelLayer"),
        "CONFIG": {
            "hosts": [(config("REDIS_HOST", default="redis"), config("REDIS_PORT", cast=int, default=6379))],
        },
    },
}

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels.layers.InMemoryChannelLayer',
#     },
# }

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',  # Higher level for Django core logging
            'propagate': True,
        },
        'channels': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',  # Ensure we capture all debug messages from Channels
            'propagate': True,
        },
        'consumers': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',  # Adjust this to your specific consumer namespace
            'propagate': False,
        },
        # Use the root logger to capture logs from other parts of the application
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',  # Default logging level for other loggers
            'propagate': True,
        },
    },
}

# ASGI and WSGI configuration
ASGI_APPLICATION = 'simulateur.asgi.application'

# Email configuration
MAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.example.com')
EMAIL_PORT = config('EMAIL_PORT', cast=int, default=587)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='your-email@example.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='your-email-password')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)

# Social account providers
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID', default='your-google-client-id'),
            'secret': config('GOOGLE_SECRET', default='your-google-client-secret'),
            'key': ''
        }
    },
    'github': {
        'APP': {
            'client_id': config('GITHUB_CLIENT_ID', default='your-github-client-id'),
            'secret': config('GITHUB_SECRET', default='your-github-client-secret'),
            'key': ''
        }
    },
    'microsoft': {
        'APP': {
            'client_id': config('MICROSOFT_CLIENT_ID', default='your-microsoft-client-id'),
            'secret': config('MICROSOFT_SECRET', default='your-microsoft-client-secret'),
            'key': ''
        }
    },
    'notion': {
        'APP': {
            'client_id': config('NOTION_CLIENT_ID', default='your-notion-client-id'),
            'secret': '',
            'key': ''
        }
    }
}

# Performance recording
PERF_REC = {
    "MODE": config("PERF_REC_MODE", default="once"),
}

# Jet settings
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

# RQ configuration
RQ_QUEUES = {
    'default': {
        'HOST': 'redis',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    },
}

# Health check settings
HEALTH_CHECK = {
    'DISK_USAGE_MAX': 90,  # percent
    'MEMORY_MIN': 100,  # in MB
}

# Swagger settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        }
    }
}

# Cache settings
CACHE_TTL = 30
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'guest_user.backends.GuestBackend',
)
