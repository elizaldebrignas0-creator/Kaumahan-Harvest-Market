from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()


@register.filter
def media_url(image_field):
    """
    Generate production-ready media URL with fallback
    """
    if not image_field:
        return static('img/product-placeholder.jpg')
    
    if hasattr(image_field, 'url'):
        url = image_field.url
        
        # Check if the file actually exists
        try:
            import os
            from django.conf import settings
            file_path = os.path.join(settings.MEDIA_ROOT, image_field.name)
            
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                return url
            else:
                # File doesn't exist or is empty, use fallback
                return static('img/product-placeholder.jpg')
        except:
            # If there's any error checking the file, use fallback
            return static('img/product-placeholder.jpg')
    
    return static('img/product-placeholder.jpg')
