
import os
from pathlib import Path
from configurations import Configuration
import datetime
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR, 'camunda')


class BaseConfiguration(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = True

    ALLOWED_HOSTS = []

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'corsheaders',
        'utils',
        # 'solo',
        'auth_',
        'task'
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.RemoteUserMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.locale.LocaleMiddleware'
    ]

    ROOT_URLCONF = 'camunda.urls'
    AUTH_USER_MODEL = 'auth_.MainUser'
    EMAIL_USE_TLS = True


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
    WSGI_APPLICATION = 'camunda.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/3.1/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT')
        }
    }

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
    WAITING_TIME_ATTEMPTS_MIN = 3

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    STATIC_URL = '/static/'
    STATIC_ROOT = "/static"
    STATICFILES_DIRS = (os.path.join(PROJECT_DIR, "static"),)

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

    SITE_URL = 'http://localhost:8000'


    REST_FRAMEWORK = {
        'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
        # 'DEFAULT_PERMISSION_CLASSES': (
        #     'rest_framework.permissions.IsAuthenticated',
        # ),
        'DEFAULT_AUTHENTICATION_CLASSES': (

            'rest_framework_simplejwt.authentication.JWTAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.BasicAuthentication',
        ),
        'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
        'EXCEPTION_HANDLER': 'utils.exceptions.custom_exception_handler',
    }
    AUTHENTICATION_BACKENDS = (
        ('django.contrib.auth.backends.ModelBackend'),
    )
    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(seconds=300),
        'REFRESH_TOKEN_LIFETIME': timedelta(seconds=12000),
    }
    CORS_ORIGIN_ALLOW_ALL = True


class Dev(BaseConfiguration):
    DEBUG = True
    ALLOWED_HOSTS = ['*']
    SITE_URL = ''
    STATIC_ROOT = '/camunda/static'
    MEDIA_ROOT = '/camunda/media'


class Prod(BaseConfiguration):
    DEBUG = False
    ALLOWED_HOSTS = ['']
    SITE_URL = ''
    CELERY_SEND_TASK_ERROR_EMAILS = False
    STATIC_ROOT = '/camunda/static'
    MEDIA_ROOT = '/camunda/media'


