from django import template
from django.templatetags.static import static

register = template.Library()


@register.filter
def media_url(image_field):
    """
    Generate media URL with fallback
    """
    if not image_field:
        return static('img/product-placeholder.jpg')
    
    if hasattr(image_field, 'url'):
        return image_field.url
    
    return static('img/product-placeholder.jpg')
