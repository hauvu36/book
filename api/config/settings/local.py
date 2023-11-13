import os  # noqa

from .common import *  # type: ignore # noqa: F401
from .common import INSTALLED_APPS, MIDDLEWARE, TEMPLATES, env

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool("DEBUG", default=True)
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG
ALLOWED_HOSTS = ["*"]


# django-debug-toolbar
# ------------------------------------------------------------------------------
INSTALLED_APPS += ("debug_toolbar",)
MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

# django-extensions & nose test
# ------------------------------------------------------------------------------
INSTALLED_APPS += ("django_extensions",)
