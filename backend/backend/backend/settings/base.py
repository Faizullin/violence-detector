from django.utils.translation import gettext_lazy as _
import os
from datetime import timedelta

import environ

# from celery.schedules import crontab

root = environ.Path(__file__) - 3
BASE_DIR = root()
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = env.bool('DEBUG', True)
SECRET_KEY = env.str('SECRET_KEY', None)
USE_HTTPS = env.bool('USE_HTTPS', False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
FRONTEND_APP_BASE_URL = env.str(
    'FRONTEND_APP_BASE_URL', 'http://localhost:5173')
SITE_COMMAND = env.str('SITE_COMMAND', None)
EMAIL_SERVICE_NAME = env.str("EMAIL_SERVICE_NAME", None)
INSTALLED_APPS = [
    'apps.admin_dashboard',
    # 'django_restful_admin',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    "rest_framework_api_key",
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'dj_rest_auth',
    # 'dj_rest_auth.registration',
    "drf_standardized_errors",
    'django_filters',
    # 'django_celery_results',
    # 'django_celery_beat',
    # 'parler',
    # 'gmailapi_backend',
    # 'django_grapesjs',
    "log_viewer",
    'apps.accounts',
    'apps.blogs',
    # 'apps.products',
    'apps.notification_system',
    'apps.file_system',
    # 'apps.checkout',
    # 'apps.carts',
    # 'apps.contact_us',
    'apps.pages',
    # 'apps.chats',
    "apps.devices",
    "apps.violence_detection"
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = None
if env.str("DB_USER", None) is not None and env.str("DB_PASSWORD", None) is not None:
    DATABASES = {
        'default': {
            'ENGINE': env.str('DB_ENGINE'),
            'NAME': env.str('DB_NAME'),
            'USER': env.str('DB_USER'),
            'PASSWORD': env.str('DB_PASSWORD'),
            'HOST': env.str('DB_HOST'),
            'PORT': env.str('DB_PORT'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# USE_I18N = True
LANGUAGE_CODE = env.str('LANGUAGE_CODE', 'en-us')
TIME_ZONE = env.str('TIME_ZONE', 'Asia/Almaty')

LANGUAGES = [
    ('kk', _('Kazakh')),
    ('en-us', _('English')),  # Add other languages if necessary
    ('ru', _('Russian')),  # Add other languages if necessary
]
# PARLER_LANGUAGES = {
#     None: (
#         {'code': 'en-us', },
#         {'code': 'ru', },
#     ),
#     'default': {
#         'fallback': 'en-us',
#         'hide_untranslated': False,
#     }
# }
# PARLER_DEFAULT_LANGUAGE_CODE = 'en-us'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

public_root = root.path('public/')
MEDIA_ROOT = public_root('media')
MEDIA_URL = env.str('MEDIA_URL', default='media/')
STATIC_ROOT = public_root('static')
STATIC_URL = env.str('STATIC_URL', default='static/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SITE_ID = 1

# REST_FRAMEWORK settings

REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%m/%d/%Y %I:%M%P",
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        # 'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler"
}


# REST_AUTH = {
#     'USE_JWT': True,
#     "JWT_AUTH_COOKIE": "my-app-auth",  # Name of access token cookie
#     "JWT_AUTH_REFRESH_COOKIE": "my-app-refresh",  # Name of refresh token cookie
#     'JWT_AUTH_HTTPONLY': False,
#     'JWT_AUTH_RETURN_EXPIRATION': True,
#     'JWT_SERIALIZER_WITH_EXPIRATION': 'apps.accounts.serializers.JWTSerializerWithExpiration',
#     'SESSION_LOGIN': False,
# }
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
# }
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# ACCOUNT_ADAPTER = 'apps.accounts.adapters.AccountAdapter'
# AUTHENTICATION_BACKENDS = [
#     'allauth.account.auth_backends.AuthenticationBackend',
#     'django.contrib.auth.backends.ModelBackend',
# ]
AUTH_USER_MODEL = 'accounts.CustomUser'
# LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/login"
# ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None

if EMAIL_SERVICE_NAME == "GMAIL_OAUTH":
    EMAIL_SEND_FROM_NAME = env.str("EMAIL_SEND_FROM_NAME", None)
    EMAIL_BACKEND = 'gmailapi_backend.mail.GmailBackend'
    GMAIL_API_CLIENT_ID = env.str("GMAIL_API_CLIENT_ID")
    GMAIL_API_CLIENT_SECRET = env.str("GMAIL_API_CLIENT_SECRET")
    GMAIL_API_REFRESH_TOKEN = env.str("GMAIL_API_REFRESH_TOKEN")
elif env.str("EMAIL_HOST_USER", None) is not None:
    EMAIL_SEND_FROM_NAME = env.str("EMAIL_SEND_FROM_NAME")
    EMAIL_HOST = env.str("EMAIL_HOST")
    EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = env.str("EMAIL_PORT")
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True

# CSRF_TRUSTED_ORIGINS = [FRONTEND_APP_BASE_URL, ]
if USE_HTTPS:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
#
# # CELERY SETINGS
#
# CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', None)
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_TIMEZONE = TIME_ZONE
# CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', None)
#
# CELERY_BEAT_SCHEDULE = {
#     "check_booking_payments": {
#         "task": "bookings.tasks.check_booking_payments",
#         "schedule": crontab(minute='*/10'),  # Run every 10 minutes ('*/10')
#     }
# }

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': CELERY_BROKER_URL,
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }


USE_VIOLENCE_DETECTION = env.bool('USE_VIOLENCE_DETECTION', False)