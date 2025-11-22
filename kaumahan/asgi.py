"""ASGI config for Kaumahan Harvest Market project."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kaumahan.settings")

application = get_asgi_application()
