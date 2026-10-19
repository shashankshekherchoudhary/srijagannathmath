import os
import sys
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

IS_TESTING = 'test' in sys.argv

# SECURITY WARNING: don't run with debug turned on in production!
# Set DEBUG=False in production via environment variable.
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

# SECURITY WARNING: keep the secret key used in production secret!
# Use environment variable; provide fallback for build-time analysis (e.g. Vercel build, Docker build)
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-prod-placeholder-key-please-set-secret-key-in-dashboard-50-chars'
)

# Allowed hosts configuration
_raw_hosts = os.environ.get('ALLOWED_HOSTS')
if _raw_hosts:
    ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(',') if h.strip()]
elif IS_TESTING:
    ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']
else:
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        '[::1]',
        '.vercel.app',
        '.railway.app',
        '.up.railway.app',
        '.onrender.com',
    ]

# CSRF trusted origins for Vercel, Railway, and custom domains
_raw_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://*.railway.app',
    'https://*.up.railway.app',
] + [c.strip() for c in _raw_csrf.split(',') if c.strip()]

# Reverse proxy SSL header (essential for Railway/Cloudflare HTTPS termination)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Production Security Headers
if not DEBUG and not IS_TESTING:
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() in ('true', '1', 'yes')
    SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '31536000'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'

# Session hardening (applies in all modes)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 3600  # 1 hour for admin sessions
SESSION_COOKIE_SAMESITE = 'Lax'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'core',
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
                'core.context_processors.temple_info_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Persistent directory support (useful for Railway Volume, Docker mount, or serverless /tmp)
if os.environ.get('VERCEL'):
    default_data_dir = Path('/tmp')
else:
    default_data_dir = BASE_DIR

DATA_DIR = Path(os.environ.get('DATA_DIR', default_data_dir))
try:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
except (PermissionError, OSError):
    DATA_DIR = Path('/tmp')
    DATA_DIR.mkdir(parents=True, exist_ok=True)

# Database (Supports PostgreSQL via DATABASE_URL; defaults to SQLite)
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{DATA_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# In-Memory Cache (reduces duplicate DB hits for singleton institutional data)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'sri-jagannath-math-cache',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Whitenoise storage for compression and caching
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}
WHITENOISE_MANIFEST_STRICT = False

# Cloudinary Media Storage (Active if credentials or CLOUDINARY_URL are set)
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

if CLOUDINARY_URL or CLOUDINARY_CLOUD_NAME:
    STORAGES['default'] = {
        'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
    }
    if CLOUDINARY_CLOUD_NAME:
        CLOUDINARY_STORAGE = {
            'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
            'API_KEY': CLOUDINARY_API_KEY,
            'API_SECRET': CLOUDINARY_API_SECRET,
        }

MEDIA_URL = '/media/'
MEDIA_ROOT = DATA_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Production Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'core': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

