"""
Настройки бэкэнда для локального запуска.
"""

from .base import *

SECRET_KEY = "django-insecure-hi59)g6r&kz_j$3-lroc7n6x$zm$u)b(6tc8_6nb*ml*mzc8kd"

DEBUG = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "/static/"

MEDIA_URL = "media/"