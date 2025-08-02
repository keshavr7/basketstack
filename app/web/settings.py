"""
Django settings for django-query-app project.
"""

import os
from pathlib import Path

import dj_database_url

from .config import Config

# Initialize config
config = Config()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", "")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.bool("DEBUG", False)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", "localhost").split(",")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "django_celery_beat",
    "jsoneditor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "web.config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB", "postgres"),
        "USER": config("POSTGRES_USER", "postgres"),
        "PASSWORD": config("POSTGRES_PASSWORD", "PaSsw0rd"),
        "HOST": config("POSTGRES_HOST", "db"),
        "PORT": config("POSTGRES_PORT", 5432),
    }
}

DATABASE_URL = config("DATABASE_URL", None)
if DATABASE_URL:
    DATABASES["default"] = dj_database_url.parse(DATABASE_URL)


# Memory caches
REDIS_URL = config("REDIS_URL", "redis://localhost:6379/0")


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(os.path.join(os.path.dirname(BASE_DIR), "public"), "staticfiles")
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

#
# Set up logging
#
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "%(asctime)s %(processName)s %(process)d %(thread)d "
                "%(levelname)s %(module)s %(message)s"
            )
        },
        "normal": {
            "format": "%(asctime)s <%(process)d> %(levelname)s [%(name)s] (%(module)s) %(message)s"
        },
        "tasks": {
            "format": (
                "%(asctime)s %(processName)s %(levelname)s %(task_name)s "
                "%(task_id)s %(module)s %(message)s"
            )
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": [],
            "class": "logging.StreamHandler",
            "formatter": "normal",
        },
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["console"],
        },
        "django": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# REST Framework configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
}


# Celery configuration
CELERY_BROKER_URL = config("CELERY_BROKER_URL", REDIS_URL)

# Disable broker connection pooling
CELERY_BROKER_POOL_LIMIT = config.int("CELERY_BROKER_POOL_LIMIT", 0)
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "visibility_timeout": config.int("CELERY_BROKER_VISIBILITY_TIMEOUT", 3600)
}
CELERY_TASK_ACKS_LATE = 1
# CELERY_TASK_ACKS_ON_FAILURE_OR_TIMEOUT = 1
CELERY_TASK_REJECT_ON_WORKER_LOST = 1
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND = None
CELERY_TIMEZONE = TIME_ZONE
# Celery logging
CELERY_WORKER_LOG_FORMAT = LOGGING["formatters"]["normal"]["format"]
CELERY_WORKER_TASK_LOG_FORMAT = LOGGING["formatters"]["tasks"]["format"]


# JSON EDITOR
# https://c9.io/nnseva/django-jsoneditor/
JSON_EDITOR_JS = "https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/8.6.4/jsoneditor.js"
JSON_EDITOR_CSS = "https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/8.6.4/jsoneditor.css"
