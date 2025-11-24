from django import template
from django.templatetags.static import static
from django.conf import settings

register = template.Library()

@register.simple_tag
def product_image_url(product):
    """
    Returns the correct product image URL with proper fallback handling.
    Ensures images always load from media/products/ and never fall back to logo.
    """
    if not product:
        return static('img/product-placeholder.jpg')
    
    # Check if product has an image
    if hasattr(product, 'image') and product.image:
        # Check if image has a URL attribute and it's not empty
        if hasattr(product.image, 'url') and product.image.url:
            image_url = product.image.url
            # Ensure it's a media/products URL
            if image_url.startswith('/media/products/'):
                return image_url
            else:
                # Log warning and use fallback
                print(f"Warning: Product image URL doesn't start with /media/products/: {image_url}")
                return static('img/product-placeholder.jpg')
        else:
            # Image exists but no URL - use fallback
            return static('img/product-placeholder.jpg')
    else:
        # No image - use fallback
        return static('img/product-placeholder.jpg')

@register.simple_tag
def product_image_tag(product, css_class='', alt_text=''):
    """
    Returns a complete img tag for product image with proper fallback.
    """
    image_url = product_image_url(product)
    
    if not alt_text and product:
        alt_text = product.name
    
    attrs = []
    if css_class:
        attrs.append(f'class="{css_class}"')
    
    return f'<img src="{image_url}" alt="{alt_text}" {" ".join(attrs)} loading="lazy">'

@register.filter
def has_valid_image(product):
    """
    Check if product has a valid image that should load correctly.
    """
    if not product or not hasattr(product, 'image') or not product.image:
        return False
    
    if not hasattr(product.image, 'url') or not product.image.url:
        return False
    
    # Ensure it's a media/products URL
    return product.image.url.startswith('/media/products/')

@register.simple_tag
def debug_product_image(product):
    """
    Debug function to show product image information.
    """
    debug_info = {
        'product_name': getattr(product, 'name', 'Unknown'),
        'has_image': hasattr(product, 'image') and bool(product.image),
        'image_field': str(getattr(product, 'image', 'None')),
        'image_url': getattr(product.image, 'url', None) if hasattr(product, 'image') and product.image else None,
        'is_media_url': False,
        'is_valid_url': False
    }
    
    if debug_info['image_url']:
        debug_info['is_media_url'] = debug_info['image_url'].startswith('/media/products/')
        debug_info['is_valid_url'] = debug_info['is_media_url']
    
    return debug_info
