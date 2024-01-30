"""
Django settings for agriproject project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u1)f0vxgx448%*(ke%!936qs&$nomx#a+-e16_-#jir-*scu0#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5', # bootstrap
    'precisionagri', # pas
    'django_recaptcha', # captcha 
    # for third party
    'django.contrib.sites', 
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # social Providers
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    # Restframework for creating api 
    'rest_framework', 
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'agriproject.urls'

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

WSGI_APPLICATION = 'agriproject.wsgi.application'


#Recaptcha key

RECAPTCHA_PUBLIC_KEY = "6LcKsNglAAAAALIMgjrwzsFTbojqMzx_SUm1qshu"
RECAPTCHA_PRIVATE_KEY= "6LcKsNglAAAAAJHqZJaze5nzZWv_IUgccHGf0_Hg"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'railway',
        'USER': 'root',
        'PASSWORD':'4bdcDCbgf35ggde45B4C5C4BcDBD1gE-', 
        'HOST': 'monorail.proxy.rlwy.net',
        'PORT': '38100',
    }
}
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


STATIC_URL = 'static/'
STATIC_ROOT= BASE_DIR / 'static'
MEDIA_URL = 'ml/'
MEDIA_ROOT =  BASE_DIR / 'ml'
MEDIA_DIRS = [MEDIA_ROOT]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'brsapp33@gmail.com'
EMAIL_HOST_PASSWORD = 'sqkeczqcyydloipa'
EMAIL_USE_TLS = 'True'


LOGOUT_REDIRECT_URL = 'home'

LOGIN_REDIRECT_URL = 'home'
 

AUTH_USER_MODEL = 'precisionagri.User'

# Third party Authentication details
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

# credentials for google 
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "17801722881-apjj45mlr6lr75t153i3p5t6dhe4v7k7.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "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"

# facebook credentials facebook
SOCIAL_AUTH_FACEBOOK_OAUTH2_KEY = "1440793079838730"
SOCIAL_AUTH_FACEBOOK_OAUTH2_SECRET = "5bbfcf1561e4f03b1da7b651cd58b652"

SITE_ID = 1 
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 3
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
ACCOUNT_UNIQUE_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'METHOD': 'oauth2',
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'facebook': {
        'METHOD': 'oauth2', 
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v13.0',
        'GRAPH_API_URL': 'https://graph.facebook.com/v13.0',
    }
}

# twilio credentials part
TWILIO_ACCOUNT_SID = 'AC4f5299ff9ddabce3f04fe02d195ca8a6'
TWILIO_AUTH_TOKEN = '9e5b95bd3107d32744010b81444ee1bc'
TWILIO_PHONE_NUMBER = '+18622440340'
