"""Contain root settings for Django Application."""

import os
from pathlib import Path

import sentry_sdk
from django.core.management.utils import get_random_secret_key
from sentry_sdk.integrations.django import DjangoIntegration

SENTRY_DSN_1 = os.getenv("SENTRY_DSN_1", None)
SENTRY_DSN_2 = os.getenv("SENTRY_DSN_2", None)
SENTRY_SAMPLE_RATE = os.getenv("SENTRY_SAMPLE_RATE", "1.0")

if SENTRY_DSN_1 is not None and SENTRY_DSN_2 is not None:
    sentry_sdk.init(
        dsn=f"https://{SENTRY_DSN_1}.ingest.sentry.io/{SENTRY_DSN_2}",
        integrations=[DjangoIntegration()],
        traces_sample_rate=float(SENTRY_SAMPLE_RATE),
        send_default_pii=True,
    )


BASE_DIR = Path(__file__).resolve().parent.parent

SITE_ID = 1

SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())
HASHID_FIELD_SALT = os.getenv("HASHID_FIELD_SALT", get_random_secret_key())

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Application definition

INSTALLED_APPS = [
    # defaults
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # custom
    "users",
]

AUTH_USER_MODEL = "users.CustomUser"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database

if os.getenv("DJANGO_DEVELOPMENT", 0) == "1":
    # local development
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.getenv("POSTGRES_NAME"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("POSTGRES_HOST"),
            "PORT": os.getenv("POSTGRES_PORT"),
        }
    }

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"
STATICFILES_DIRS = (str(BASE_DIR.joinpath("static")),)
STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": "debug.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": True,
        },
    },
    "root": {
        "handlers": ["file"],
        "level": "WARNING",
    },
}

# Producution settings
DEBUG = False
ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    # TODO: where is this going to be hosted?
]
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Development settings
if os.getenv("DJANGO_DEVELOPMENT", 0) == "1":
    DEBUG = True
    ALLOWED_HOSTS = ["*"]
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    del SECURE_PROXY_SSL_HEADER
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
