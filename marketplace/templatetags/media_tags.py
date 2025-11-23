from django import template
from django.conf import settings

register = template.Library()


@register.filter
def media_url(image_field):
    """
    Generate production-ready media URL
    In production, use the custom media serving view
    """
    if not image_field:
        return ''
    
    if hasattr(image_field, 'url'):
        # For production deployment, ensure the URL uses our custom media serving
        url = image_field.url
        if settings.DEBUG:
            # Development - use standard media URL
            return url
        else:
            # Production - use our custom media serving URL
            return url  # The URL pattern will handle it
    return ''
