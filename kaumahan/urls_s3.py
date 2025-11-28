"""
URL Configuration for AWS S3 Storage
Handles both development and production environments
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path("marketplace/", include("marketplace.urls")),
]

# Development: Serve media files locally
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Production: Media files served from S3, static from whitenoise
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
