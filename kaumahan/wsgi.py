"""WSGI config for Kaumahan Harvest Market project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kaumahan.settings")

application = get_wsgi_application()
