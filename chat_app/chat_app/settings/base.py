"""
Django settings for chat_app project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from datetime import timedelta
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

root = environ.Path(BASE_DIR)  # get root of the project
env = environ.Env()
environ.Env.read_env()  # reading .env file


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

# CORS Settings
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = env.list(
    'CORS_ORIGIN_WHITELIST', default=['http://localhost:8080', 'http://127.0.0.1:8080']
)
ALLOWED_HOSTS = env.list(
    'ALLOWED_HOSTS', default=['localhost', '127.0.0.1']
)

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'drf_yasg',
    'rest_framework',
    'django_rest_passwordreset',
    'django_filters',
    'channels',
]

USER_APPS = [
    'apps.chats',
    'apps.users',
    'apps.utils'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + USER_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}

ROOT_URLCONF = 'chat_app.urls'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'chat_app.wsgi.application'
ASGI_APPLICATION = 'chat_app.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env.str('DATABASE_HOST', default='localhost'),
        'NAME': env.str('DATABASE_NAME', default='workshop_manager'),
        'USER': env.str('DATABASE_USER', default='postgres'),
        'PASSWORD': env.str('DATABASE_PASSWORD', default='postgres')
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 3}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# User Model to use.
AUTH_USER_MODEL = 'users.User'

# JWT Config
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True
}

# Email settings
EMAIL_BACKEND = env.str(
    'EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend'
)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST = env.str('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', default='')

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = Path.joinpath(BASE_DIR, 'static/')

# Uploads URL
MEDIA_URL = '/media_uploads/'
MEDIA_ROOT = Path.joinpath(BASE_DIR, 'media_uploads')

# CELERY SETTINGS
BROKER_URL = env.str('BROKER_URL', default='redis://localhost:6379')
CELERY_RESULT_BACKEND = env.str(
    'CELERY_RESULT_BACKEND', default='redis://localhost:6379'
)
CELERY_ACCEPT_CONTENT = env.list(
    'CELERY_ACCEPT_CONTENT', default=['application/json']
)
CELERY_TIMEZONE = env.str('CELERY_TIMEZONE', default='Europe/Berlin')
CELERY_ENABLE_UTC = False
BROKER_USE_SSL = env.bool('CELERY_BROKER_USE_SSL', default=False)
CELERY_BEAT_SCHEDULER = env.bool('CELERY_BEAT_SCHEDULER', 'django_celery_beat.schedulers:DatabaseScheduler')

# Frontend URL
FRONTEND_PASSWORD_RESET_URL = env.str(
    'FRONTEND_PASSWORD_RESET_URL', default='')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME = 1

if env.bool('DEBUG', default=False):
    INSTALLED_APPS += [
        'debug_toolbar'
    ]
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = [
        '127.0.0.1',
    ]
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].insert(
        0, 'rest_framework.authentication.BasicAuthentication')
