/**
 * Enhanced Image Loading Handler for Kaumahan Harvest Market
 * Ensures consistent image loading and provides fallbacks in production
 */

class ImageHandler {
    constructor() {
        this.fallbackUrl = '/static/img/product-placeholder.jpg';
        this.loadedImages = new Set();
        this.failedImages = new Set();
        this.retryAttempts = new Map();
        this.maxRetries = 3;
        this.isProduction = !window.location.hostname.includes('localhost') && !window.location.hostname.includes('127.0.0.1');
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
        
        // Only add production optimizations in actual production
        if (this.isProduction) {
            setTimeout(() => this.addProductionOptimizations(), 2000);
        }
        
        // Setup periodic retry mechanism only in production
        if (this.isProduction) {
            this.setupPeriodicRetry();
        }
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
        
        // Production logging
        if (this.isProduction) {
            console.warn('Production - Image failed to load:', src);
        } else {
            console.warn('Development - Image failed to load:', src);
        }
        
        // Check if it's already using fallback
        if (src.includes('product-placeholder.jpg')) {
            console.warn('Fallback image also failed to load:', src);
            return;
        }

        // IMPORTANT: Never use logo as fallback - always use product placeholder
        const fallbackWithTimestamp = this.fallbackUrl + '?t=' + Date.now();
        img.src = fallbackWithTimestamp;
        img.classList.add('img-fallback');
        
        // Add error handling class
        img.classList.add('image-load-error');
        
        // Log the original failed image for debugging
        console.log('Image failed, using fallback:', {
            original: src,
            fallback: fallbackWithTimestamp,
            isMedia: src.includes('/media/'),
            isStatic: src.includes('/static/'),
            isProductImage: src.includes('/media/products/')
        });
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
            // In development, only handle obviously broken images
            if (!this.isProduction) {
                if (!img.complete) {
                    // Add loading state for images still loading
                    img.classList.add('image-loading');
                } else if (img.naturalWidth === 0 || img.naturalHeight === 0) {
                    // Only handle truly broken images
                    this.handleFailedImage(img);
                } else {
                    // Successfully loaded
                    this.handleSuccessfulImage(img);
                }
            } else {
                // In production, be more careful with validation
                if (!img.complete) {
                    img.classList.add('image-loading');
                } else if (img.naturalWidth === 0 || img.naturalHeight === 0) {
                    this.handleFailedImage(img);
                } else {
                    this.handleSuccessfulImage(img);
                }
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

    addProductionOptimizations() {
        // Only add cache-busting to images that have actually failed and are media files
        const failedMediaImages = document.querySelectorAll('.image-load-error[src*="/media/products/"]');
        failedMediaImages.forEach(img => {
            if (!img.src.includes('?t=') && !img.src.includes('?retry=')) {
                console.log('Adding cache-busting to failed media image:', img.src);
                const separator = img.src.includes('?') ? '&' : '?';
                img.src = img.src + separator + 't=' + Date.now();
            }
        });
        
        // Only validate for actual logo issues, don't interfere with normal images
        this.validateMediaImages();
    }
    
    validateMediaImages() {
        // Only check for actual logo files in media directory, don't interfere with product images
        const problematicImages = document.querySelectorAll('img[src*="/media/"][src*="logo"], img[src*="/media/"][src*="banner"], img[src*="/media/"][src*="favicon"]');
        problematicImages.forEach(img => {
            console.warn('Invalid media image detected (logo/banner in media):', img.src);
            img.src = this.fallbackUrl + '?t=' + Date.now();
            img.classList.add('img-fallback');
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
            total: document.querySelectorAll('img').length,
            isProduction: this.isProduction
        };
    }

    // Method to manually retry all failed images
    retryFailedImages() {
        const failedImages = document.querySelectorAll('.image-load-error');
        failedImages.forEach(img => {
            const originalSrc = img.src.split('?')[0];
            if (!originalSrc.includes('product-placeholder.jpg')) {
                img.src = originalSrc + '?manual_retry=' + Date.now();
            }
        });
    }

    // Production-specific validation method
    validateMediaUrls() {
        if (!this.isProduction) return;
        
        const mediaImages = document.querySelectorAll('img[src*="/media/"]');
        console.log(`Validating ${mediaImages.length} media images in production`);
        
        let issuesFound = 0;
        mediaImages.forEach(img => {
            const url = new URL(img.src);
            if (!url.pathname.startsWith('/media/')) {
                console.warn('Invalid media URL detected:', img.src);
                issuesFound++;
            }
            
            if (img.src.includes('logo') || img.src.includes('banner')) {
                console.error('CRITICAL: Logo/banner found in media URLs:', img.src);
                issuesFound++;
            }
        });
        
        if (issuesFound > 0) {
            console.error(`Found ${issuesFound} media image issues in production`);
        } else {
            console.log('All media images validated successfully');
        }
    }
    
    // Method to test image loading
    testImageLoading() {
        console.log('=== IMAGE LOADING TEST ===');
        const productImages = document.querySelectorAll('img[src*="/media/products/"]');
        
        console.log(`Found ${productImages.length} product images`);
        
        productImages.forEach((img, index) => {
            console.log(`Image ${index + 1}:`, {
                src: img.src,
                complete: img.complete,
                naturalWidth: img.naturalWidth,
                naturalHeight: img.naturalHeight,
                classes: img.className,
                hasError: img.classList.contains('image-load-error'),
                isLoading: img.classList.contains('image-loading'),
                isLoaded: img.classList.contains('image-loaded')
            });
            
            // Test if image actually loads
            if (!img.complete || img.naturalWidth === 0) {
                console.warn(`Image ${index + 1} may not be loading properly:`, img.src);
            }
        });
        
        return {
            total: productImages.length,
            loaded: document.querySelectorAll('img.image-loaded[src*="/media/products/"]').length,
            failed: document.querySelectorAll('img.image-load-error[src*="/media/products/"]').length,
            loading: document.querySelectorAll('img.image-loading[src*="/media/products/"]').length
        };
    }
    
    // Method to force reload all product images
    forceReloadProductImages() {
        const productImages = document.querySelectorAll('img[src*="/media/products/"]');
        console.log(`Force reloading ${productImages.length} product images`);
        
        productImages.forEach(img => {
            const originalSrc = img.src.split('?')[0];
            const newSrc = originalSrc + '?force_reload=' + Date.now();
            
            // Remove error states
            img.classList.remove('image-load-error', 'image-loaded');
            img.classList.add('image-loading');
            
            // Clear from tracking sets
            this.loadedImages.delete(img.src);
            this.failedImages.delete(img.src);
            
            // Reload with new timestamp
            img.src = newSrc;
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
    
    /* Production-specific styles */
    .production-warning {
        background: rgba(255, 193, 7, 0.1);
        border: 1px solid #ffc107;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.5rem 0;
        font-size: 0.875rem;
        color: #856404;
    }
`;

// Inject styles
const styleSheet = document.createElement('style');
styleSheet.textContent = imageHandlerStyles;
document.head.appendChild(styleSheet);

// Make available globally for debugging
window.imageStats = () => window.imageHandler.getImageStats();
window.retryImages = () => window.imageHandler.retryFailedImages();
window.validateMedia = () => window.imageHandler.validateMediaUrls();
window.testImages = () => window.imageHandler.testImageLoading();
window.reloadImages = () => window.imageHandler.forceReloadProductImages();

// Auto-retry failed images after page load (only in production)
setTimeout(() => {
    if (window.imageHandler.isProduction) {
        window.imageHandler.retryFailedImages();
        window.imageHandler.validateMediaUrls();
    }
}, 2000);

// Periodic validation only in production (every 30 seconds)
if (window.imageHandler.isProduction) {
    setInterval(() => {
        window.imageHandler.validateMediaImages();
    }, 30000);
}
