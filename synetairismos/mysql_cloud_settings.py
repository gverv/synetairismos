"""
MySQL on Oracle Cloud Compute Instance settings
"""
from .settings import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Add your Oracle Cloud VM IP and domain
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '150.230.115.0',  # Oracle Cloud VM Public IP
    'django-synetairismos.com',  # Your domain if you have one
]

# Database for MySQL on Oracle Cloud Compute Instance
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'synet_db',
        'USER': 'synet_user',
        'PASSWORD': 'pefkos@@1932',  # Change this to your secure password
        'HOST': '10.0.0.48',  # Oracle Cloud VM Private IP (use SSH tunnel for external access)
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# Static files configuration for production
STATIC_URL = '/static/'
STATIC_ROOT = '/home/django/synetairismos/staticfiles/'

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Session settings optimized for Oracle Cloud
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_COOKIE_SECURE = False  # Set to True when you enable HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_NAME = 'synet_sessionid'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/home/django/synetairismos/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
