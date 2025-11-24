from django import template
from django.templatetags.static import static

register = template.Library()


@register.filter
def media_url(image_field):
    """
    Generate media URL with robust fallback handling
    """
    if not image_field:
        return static('img/product-placeholder.jpg')
    
    # Check if image field has a valid URL
    if hasattr(image_field, 'url') and image_field.url:
        return image_field.url
    
    return static('img/product-placeholder.jpg')


@register.simple_tag
def safe_static(path):
    """
    Safe static file loading with error handling
    """
    try:
        return static(path)
    except:
        return ''


@register.filter
def image_with_fallback(image_field, fallback_path='img/product-placeholder.jpg'):
    """
    Enhanced image filter with multiple fallback options
    """
    if not image_field:
        return static(fallback_path)
    
    if hasattr(image_field, 'url') and image_field.url:
        return image_field.url
    
    return static(fallback_path)
