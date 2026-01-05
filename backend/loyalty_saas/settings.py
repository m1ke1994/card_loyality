import os
from datetime import timedelta
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, "change_me"),
    ALLOWED_HOSTS=(str, "localhost,127.0.0.1"),
    CORS_ALLOWED_ORIGINS=(str, ""),
    CSRF_TRUSTED_ORIGINS=(str, ""),
    DATABASE_URL=(str, "postgres://postgres:postgres@localhost:5432/loyalty"),
    REDIS_URL=(str, "redis://localhost:6379/0"),
    TELEGRAM_BOT_TOKEN=(str, ""),
    JWT_ACCESS_TTL_MIN=(int, 15),
    JWT_REFRESH_TTL_DAYS=(int, 30),
    QR_TOKEN_TTL_SEC=(int, 30),
    LOGIN_TOKEN_TTL_SEC=(int, 300),
    ACTIVE_VISIT_AUTO_CLOSE_HOURS=(int, 6),
    TENANT_HEADER=(str, "HTTP_X_TENANT_SLUG"),
)

environ.Env.read_env(os.path.join(BASE_DIR, "..", ".env"))


def split_list(value: str, fallback=None):
    if value is None:
        return fallback or []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [item.strip() for item in str(value).split(",") if item.strip()]


SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = split_list(env("ALLOWED_HOSTS"), ["localhost"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "drf_spectacular",
    "apps.tenants",
    "apps.accounts",
    "apps.telegram_auth",
    "apps.loyalty",
    "apps.coupons",
    "apps.promotions",
    "apps.audit",
    "apps.reports",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.tenants.middleware.TenantMiddleware",
]

ROOT_URLCONF = "loyalty_saas.urls"

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

WSGI_APPLICATION = "loyalty_saas.wsgi.application"
ASGI_APPLICATION = "loyalty_saas.asgi.application"

DATABASES = {"default": env.db("DATABASE_URL")}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
APPEND_SLASH = False

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("apps.accounts.authentication.JWTAuthentication",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Loyalty SaaS API",
    "DESCRIPTION": "Multi-tenant loyalty platform with Telegram auth and QR tokens.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env("JWT_ACCESS_TTL_MIN")),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=env("JWT_REFRESH_TTL_DAYS")),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "UPDATE_LAST_LOGIN": False,
}

CORS_ALLOWED_ORIGINS = split_list(env("CORS_ALLOWED_ORIGINS"), [])
CSRF_TRUSTED_ORIGINS = split_list(env("CSRF_TRUSTED_ORIGINS"), [])
CORS_ALLOW_CREDENTIALS = True

REDIS_URL = env("REDIS_URL")
TENANT_HEADER = env("TENANT_HEADER")
TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN")
QR_TOKEN_TTL_SEC = env("QR_TOKEN_TTL_SEC")
LOGIN_TOKEN_TTL_SEC = env("LOGIN_TOKEN_TTL_SEC")
ACTIVE_VISIT_AUTO_CLOSE_HOURS = env("ACTIVE_VISIT_AUTO_CLOSE_HOURS")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_BEAT_SCHEDULE = {
    "auto-close-active-visits": {
        "task": "apps.loyalty.tasks.auto_close_active_visits",
        "schedule": 300,
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "redact_auth": {
            "()": "apps.audit.logging.RedactAuthorizationFilter",
        }
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "filters": ["redact_auth"]},
    },
    "loggers": {
        "django.request": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "apps": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}
