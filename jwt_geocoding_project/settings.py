
from datetime import timedelta
import pymysql

pymysql.install_as_MySQLdb()

import os
from dotenv import load_dotenv

load_dotenv()

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    # 'django.contrib.staticfiles',
    'auth_app',
    'security_app',
    'user_app',
    'django_apscheduler',
    'student_mongodb_app'
]



MIDDLEWARE = [
    # 'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'security_app.middleware.token_required',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jwt_geocoding_project.urls'

TEMPLATES = [
    # {
    #     'BACKEND': 'django.template.backends.django.DjangoTemplates',
    #     'DIRS': [],
    #     'APP_DIRS': True,
    #     'OPTIONS': {
    #         'context_processors': [
    #             'django.template.context_processors.debug',
    #             'django.template.context_processors.request',
    #             'django.contrib.auth.context_processors.auth',
    #             'django.contrib.messages.context_processors.messages',
    #         ],
    #     },
    # },
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.getenv('REDIS_DB_URI'),
        "TIMEOUT": os.getenv('REDIS_DEFAULT_TIMEOUT')
    }
}

WSGI_APPLICATION = 'jwt_geocoding_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD')
    },
    'replica':{
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD')
    },
    'mongodb':{
        'ENGINE':'djongo',
        'NAME' : os.getenv('MONGODB_NAME'),
        'HOST': 'localhost', 
        'PORT': 27017, 
    }
}

DATABASE_ROUTERS = ['jwt_geocoding_project.dbroute.CustomRouter']


AUTH_PASSWORD_VALIDATORS = []


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JWT_TOKEN_TIME = os.getenv('JWT_ACCESS_TOKEN_EXPIRES')
JWT_REFRESH_TIME = os.getenv('JWT_REFRESH_TOKEN_EXPIRES')
JWT_ALGO = os.getenv('JWT_ALGO')
JWT_SECRET = os.getenv('APP_JWT_SECRET')


APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

SCHEDULER_DEFAULT = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_ID')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')

REDIS_TIMEOUT = os.getenv('DB_PASSWORD')

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')