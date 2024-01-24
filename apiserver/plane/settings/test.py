"""Test Settings"""
from .common import * # noqa

DEBUG = True

# Send it in to email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

INSTALLED_APPS.append("plane.tests",)
