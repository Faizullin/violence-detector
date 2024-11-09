from .base import *

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])

LOGS_DIR = os.path.join(BASE_DIR, 'logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {filename} {funcName} {lineno} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{asctime} {levelname} - {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            # 'filters': ['require_debug_true'],
            'formatter': 'simple',
        },
        'api_log': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'api/api.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'api_error_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'api/error.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'filters': ['require_debug_false'],
        #     'formatter': 'verbose',
        # },
        'celery_worker_logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'celery/worker.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django_project_api': {
            'handlers': ['console', 'api_log', ],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['api_error_log'],  # 'mail_admins',
            'level': 'ERROR',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console','celery_worker_logfile'],
            'level': 'INFO',
            # 'propagate': False,
        },
    },
}
