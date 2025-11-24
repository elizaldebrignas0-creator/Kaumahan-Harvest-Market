/**
 * Image Loading Handler for Kaumahan Harvest Market
 * Ensures consistent image loading and provides fallbacks
 */

class ImageHandler {
    constructor() {
        this.fallbackUrl = '/static/img/product-placeholder.jpg';
        this.loadedImages = new Set();
        this.failedImages = new Set();
        this.init();
    }

    init() {
        // Handle image loading errors globally
        document.addEventListener('error', this.handleImageError.bind(this), true);
        
        // Handle successful image loads
        document.addEventListener('load', this.handleImageLoad.bind(this), true);
        
        // Process existing images on page load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', this.processExistingImages.bind(this));
        } else {
            this.processExistingImages();
        }
        
        // Handle dynamic content changes
        this.observeContentChanges();
    }

    handleImageError(event) {
        const img = event.target;
        if (img.tagName === 'IMG') {
            this.handleFailedImage(img);
        }
    }

    handleImageLoad(event) {
        const img = event.target;
        if (img.tagName === 'IMG') {
            this.handleSuccessfulImage(img);
        }
    }

    handleFailedImage(img) {
        // Avoid infinite loops
        if (this.failedImages.has(img.src)) {
            return;
        }

        this.failedImages.add(img.src);
        
        // Check if it's already using fallback
        if (img.src.includes('product-placeholder.jpg')) {
            console.warn('Fallback image also failed to load:', img.src);
            return;
        }

        console.warn('Image failed to load, using fallback:', img.src);
        
        // Apply fallback
        img.src = this.fallbackUrl;
        img.classList.add('img-fallback');
        
        // Add error handling class
        img.classList.add('image-load-error');
    }

    handleSuccessfulImage(img) {
        this.loadedImages.add(img.src);
        img.classList.add('image-loaded');
        img.classList.remove('image-load-error');
    }

    processExistingImages() {
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            if (!img.complete) {
                // Add loading state
                img.classList.add('image-loading');
            } else if (img.naturalWidth === 0) {
                // Handle broken images that are already "complete"
                this.handleFailedImage(img);
            } else {
                // Handle successfully loaded images
                this.handleSuccessfulImage(img);
            }
        });
    }

    observeContentChanges() {
        // Watch for dynamically added images
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        const images = node.querySelectorAll ? node.querySelectorAll('img') : [];
                        images.forEach(img => {
                            if (!img.complete) {
                                img.classList.add('image-loading');
                            }
                        });
                    }
                });
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // Method to preload critical images
    preloadImages(urls) {
        urls.forEach(url => {
            if (!this.loadedImages.has(url)) {
                const img = new Image();
                img.onload = () => this.loadedImages.add(url);
                img.onerror = () => this.failedImages.add(url);
                img.src = url;
            }
        });
    }

    // Method to check if image exists
    checkImageExists(url) {
        return new Promise((resolve) => {
            const img = new Image();
            img.onload = () => resolve(true);
            img.onerror = () => resolve(false);
            img.src = url;
        });
    }

    // Method to get image stats
    getImageStats() {
        return {
            loaded: this.loadedImages.size,
            failed: this.failedImages.size,
            total: document.querySelectorAll('img').length
        };
    }
}

// Initialize the image handler
window.imageHandler = new ImageHandler();

// Add CSS for image states
const imageHandlerStyles = `
    .image-loading {
        opacity: 0.7;
        filter: blur(1px);
        transition: opacity 0.3s ease, filter 0.3s ease;
    }
    
    .image-loaded {
        opacity: 1;
        filter: none;
    }
    
    .image-load-error {
        opacity: 0.8;
        filter: grayscale(50%);
    }
    
    .img-fallback {
        border: 2px dashed #dee2e6;
        background-color: #f8f9fa;
    }
    
    /* Retry button for failed images */
    .image-retry {
        position: absolute;
        top: 5px;
        right: 5px;
        background: rgba(0, 123, 255, 0.8);
        color: white;
        border: none;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        cursor: pointer;
        font-size: 12px;
        display: none;
    }
    
    .image-load-error:hover .image-retry {
        display: block;
    }
`;

// Inject styles
const styleSheet = document.createElement('style');
styleSheet.textContent = imageHandlerStyles;
document.head.appendChild(styleSheet);

// Make available globally for debugging
window.imageStats = () => window.imageHandler.getImageStats();

// Auto-retry failed images after page load
setTimeout(() => {
    const failedImages = document.querySelectorAll('.image-load-error');
    failedImages.forEach(img => {
        if (!img.src.includes('product-placeholder.jpg')) {
            console.log('Retrying failed image:', img.src);
            const originalSrc = img.src;
            img.src = ''; // Clear to force reload
            setTimeout(() => {
                img.src = originalSrc;
            }, 100);
        }
    });
}, 2000);
