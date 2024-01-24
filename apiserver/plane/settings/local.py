"""Development settings"""
from .common import *  # noqa

DEBUG = True

# Debug Toolbar settings
INSTALLED_APPS += ("debug_toolbar",)
MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

DEBUG_TOOLBAR_PATCH_SETTINGS = False

# Only show emails in console don't send it to smtp
EMAIL_HOST="smtp.gmail.com"
EMAIL_HOST_USER="support.plane@antiersolutions.com"
EMAIL_HOST_PASSWORD="S@OrtAn208"
EMAIL_PORT=587
EMAIL_FROM="no reply<support.plane@antiersolutions.com>"
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

INTERNAL_IPS = ("127.0.0.1",)

MEDIA_URL = "/uploads/"
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:4000",
    "http://127.0.0.1:4000",
]
