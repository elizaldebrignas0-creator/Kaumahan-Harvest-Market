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
        
        // Wait a moment and check if images are actually loading
        setTimeout(() => this.checkImageLoading(), 1000);
    }

    handleImageError(event) {
        const img = event.target;
        if (img.tagName === 'IMG') {
            // Check if it's already using fallback
            if (img.src.includes('product-placeholder.jpg')) {
                console.warn('Fallback image also failed:', img.src);
                return;
            }

            // Only fallback if it's a genuine error (404, network error, etc.)
            // Don't fallback for loading issues or temporary problems
            console.warn('Image failed to load, using fallback:', img.src);
            
            // Use fallback
            img.src = this.fallbackUrl;
            img.classList.add('img-fallback');
        }
    }
    
    checkImageLoading() {
        // Check if product images are actually loading
        const productImages = document.querySelectorAll('img[src*="/media/products/"]');
        console.log(`Checking ${productImages.length} product images...`);
        
        productImages.forEach((img, index) => {
            console.log(`Image ${index + 1}:`, {
                src: img.src,
                complete: img.complete,
                naturalWidth: img.naturalWidth,
                naturalHeight: img.naturalHeight,
                hasError: img.classList.contains('img-fallback'),
                isLoaded: img.classList.contains('image-loaded')
            });
            
            // If image is complete but has no dimensions, it might be a 404
            if (img.complete && (img.naturalWidth === 0 || img.naturalHeight === 0)) {
                console.warn('Image loaded but has no dimensions - likely 404:', img.src);
                // Don't automatically fallback - let the error handler do it
            }
        });
    }
}

// Initialize the simple image handler
window.simpleImageHandler = new SimpleImageHandler();

// Make available globally for debugging
window.checkImages = () => {
    window.simpleImageHandler.checkImageLoading();
};

window.forceCheckImages = () => {
    const images = document.querySelectorAll('img[src*="/media/products/"]');
    console.log(`Force checking ${images.length} product images...`);
    
    images.forEach((img, index) => {
        // Try to reload the image if it's using fallback
        if (img.src.includes('product-placeholder.jpg')) {
            console.log(`Image ${index + 1} is using fallback, checking original...`);
            
            // Find the original product image URL from the page context
            const productCard = img.closest('.card');
            if (productCard) {
                const productName = productCard.querySelector('.card-title')?.textContent;
                console.log(`Product: ${productName}`);
                
                // You could implement logic to find the correct URL here
                // For now, just log the issue
            }
        } else {
            console.log(`Image ${index + 1}: ${img.src} (complete: ${img.complete}, size: ${img.naturalWidth}x${img.naturalHeight})`);
        }
    });
};

console.log('Simple image handler loaded - use window.checkImages() to debug');
