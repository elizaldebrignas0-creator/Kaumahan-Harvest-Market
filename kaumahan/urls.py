from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve
from django.urls import re_path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path("marketplace/", include("marketplace.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]

# Enhanced media file serving for both development and production
if settings.DEBUG:
    # Development: Django serves media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Production: Serve media files with proper caching headers
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
    
    # Ensure static files are served in production
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
