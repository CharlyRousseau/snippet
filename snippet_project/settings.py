import os
from pathlib import Path
from django.conf.urls import handler400, handler404, handler403, handler500
from django.core.management.utils import get_random_secret_key
import os
from dotenv import load_dotenv
import mimetypes

mimetypes.add_type("text/css", ".css", True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["snippet.playground-charly.fr", "127.0.0.1", "localhost"]

CSRF_TRUSTED_ORIGINS = ["https://snippet.playground-charly.fr"]

# Application definition


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "snippet",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "snippet_project.urls"

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

WSGI_APPLICATION = "snippet_project.wsgi.application"
STATIC_URL = "/static/"
STATIC_ROOT = "/app/staticfiles/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL, conn_max_age=600, ssl_require=True
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Media Configuration
IS_PRODUCTION = os.getenv("DJANGO_PRODUCTION", "False") == "True"

if IS_PRODUCTION:
    # Production settings (using MinIO or S3)
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    AWS_ACCESS_KEY_ID = os.getenv("MINIO_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY = os.getenv("MINIO_SECRET_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = os.getenv("MINIO_ENDPOINT_URL")
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False

    # MEDIA_URL should not include the bucket name directly
    MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/"
else:
    # Local development settings (using local filesystem)
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"


# Extending User

AUTH_USER_MODEL = "snippet.CustomUser"
LOGIN_REDIRECT_URL = "/"

# 4XX/5XX Handling

handler400 = "snippet.view.custom_bad_request"
handler403 = "snippet.view.custom_permission_denied"
handler404 = "snippet.view.custom_page_not_found"
handler500 = "snippet.view.custom_internal_error"
