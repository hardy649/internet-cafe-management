
from pathlib import Path
import os
from dotenv import load_dotenv

# ==========================================
# 1. Үндсэн тохиргоо
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

# .env файлаас тохиргоо унших
load_dotenv(BASE_DIR / ".env")

# Security
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "DJANGO_SECRET_KEY .env файлд байхгүй байна"
    )

DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

# ==========================================
# 2. Applications
# ==========================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Django REST Framework
    "rest_framework",

    # CORS
    "corsheaders",

    # Internet Cafe app
    "cafe",
]

# ==========================================
# 3. Middleware
# ==========================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # Flutter Web CORS
    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# ==========================================
# 4. Templates
# ==========================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ==========================================
# 5. PostgreSQL Database
# ==========================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# ==========================================
# 6. Password Validation
# ==========================================

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

# ==========================================
# 7. Language and Time
# ==========================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Ulaanbaatar"

USE_I18N = True
USE_TZ = True

# ==========================================
# 8. Static Files
# ==========================================

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==========================================
# 9. Flutter Web CORS
# ==========================================

# Localhost-ийн бүх порт зөвшөөрнө
# Зөвхөн development орчинд ашиглана

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://localhost:[0-9]+$",
    r"^http://127\.0\.0\.1:[0-9]+$",
]

# ==========================================
# 10. Django REST Framework
# ==========================================


from datetime import timedelta

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

