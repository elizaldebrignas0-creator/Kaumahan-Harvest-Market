// Simple, non-intrusive image handler
// Only handles actual errors, doesn't interfere with normal loading

class SimpleImageHandler {
    constructor() {
        this.fallbackUrl = '/static/img/product-placeholder.jpg';
        this.init();
    }

    init() {
        // Only handle actual image errors, don't interfere with normal loading
        document.addEventListener('error', this.handleImageError.bind(this), true);
        console.log('Simple image handler initialized - only handling actual errors');
    }

    handleImageError(event) {
        const img = event.target;
        if (img.tagName === 'IMG') {
            // Check if it's already using fallback
            if (img.src.includes('product-placeholder.jpg')) {
                console.warn('Fallback image also failed:', img.src);
                return;
            }

            console.warn('Image failed to load, using fallback:', img.src);
            
            // Use fallback
            img.src = this.fallbackUrl;
            img.classList.add('img-fallback');
        }
    }
}

// Initialize the simple image handler
window.simpleImageHandler = new SimpleImageHandler();

// Make available globally for debugging
window.checkImages = () => {
    const images = document.querySelectorAll('img[src*="/media/products/"]');
    console.log(`Found ${images.length} product images`);
    
    images.forEach((img, index) => {
        console.log(`Image ${index + 1}:`, {
            src: img.src,
            complete: img.complete,
            naturalWidth: img.naturalWidth,
            naturalHeight: img.naturalHeight,
            hasError: img.classList.contains('img-fallback')
        });
    });
};

console.log('Simple image handler loaded - use window.checkImages() to debug');
