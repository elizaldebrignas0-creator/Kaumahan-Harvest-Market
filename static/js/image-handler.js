/**
 * Image Loading Handler for Kaumahan Harvest Market
 * Ensures consistent image loading and provides fallbacks
 */

class ImageHandler {
    constructor() {
        this.fallbackUrl = '/static/img/product-placeholder.jpg';
        this.loadedImages = new Set();
        this.failedImages = new Set();
        this.retryAttempts = new Map();
        this.maxRetries = 3;
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
        
        // Add cache-busting for problematic images
        this.addCacheBusting();
        
        // Setup periodic retry mechanism
        this.setupPeriodicRetry();
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
        const src = img.src;
        
        // Avoid infinite loops
        if (this.failedImages.has(src)) {
            return;
        }

        this.failedImages.add(src);
        console.warn('Image failed to load:', src);
        
        // Check if it's already using fallback
        if (src.includes('product-placeholder.jpg')) {
            console.warn('Fallback image also failed to load:', src);
            return;
        }

        // Apply fallback with cache busting
        const fallbackWithTimestamp = this.fallbackUrl + '?t=' + Date.now();
        img.src = fallbackWithTimestamp;
        img.classList.add('img-fallback');
        
        // Add error handling class
        img.classList.add('image-load-error');
    }

    handleSuccessfulImage(img) {
        this.loadedImages.add(img.src);
        img.classList.add('image-loaded');
        img.classList.remove('image-load-error');
        img.classList.remove('image-loading');
        
        // Clear retry attempts for successful images
        this.retryAttempts.delete(img.src);
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

    addCacheBusting() {
        // Add cache-busting to media URLs that might be cached
        const images = document.querySelectorAll('img[src*="/media/"]');
        images.forEach(img => {
            if (!img.src.includes('?t=')) {
                const originalSrc = img.src;
                img.onload = () => this.handleSuccessfulImage(img);
                img.onerror = () => this.handleFailedImage(img);
            }
        });
    }

    setupPeriodicRetry() {
        // Retry failed images every 5 seconds
        setInterval(() => {
            const failedImages = document.querySelectorAll('.image-load-error:not(.img-fallback)');
            failedImages.forEach(img => {
                const attempts = this.retryAttempts.get(img.src) || 0;
                if (attempts < this.maxRetries) {
                    this.retryAttempts.set(img.src, attempts + 1);
                    console.log(`Retrying image (${attempts + 1}/${this.maxRetries}):`, img.src);
                    
                    // Force reload with cache busting
                    const originalSrc = img.src.split('?')[0];
                    img.src = originalSrc + '?retry=' + Date.now();
                }
            });
        }, 5000);
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

    // Method to manually retry all failed images
    retryFailedImages() {
        const failedImages = document.querySelectorAll('.image-load-error');
        failedImages.forEach(img => {
            const originalSrc = img.src.split('?')[0];
            if (!originalSrc.includes('product-placeholder.jpg')) {
                console.log('Manual retry for:', originalSrc);
                img.src = originalSrc + '?manual_retry=' + Date.now();
            }
        });
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
window.retryImages = () => window.imageHandler.retryFailedImages();

// Auto-retry failed images after page load
setTimeout(() => {
    window.imageHandler.retryFailedImages();
}, 2000);
