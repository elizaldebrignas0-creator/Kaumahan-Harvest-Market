// No image handler - let images load naturally
console.log('No image handler loaded - images will load naturally without any JavaScript interference');

// Make available globally for debugging
window.checkImages = () => {
    const images = document.querySelectorAll('img[src*="/media/products/"]');
    console.log(`Found ${images.length} product images (no handler interference)`);
    
    images.forEach((img, index) => {
        console.log(`Image ${index + 1}:`, {
            src: img.src,
            complete: img.complete,
            naturalWidth: img.naturalWidth,
            naturalHeight: img.naturalHeight,
            classes: img.className
        });
        
        // Check if image is actually loading correctly
        if (img.complete && img.naturalWidth > 0 && img.naturalHeight > 0) {
            console.log(`  ✅ Image loaded successfully`);
        } else if (img.complete && (img.naturalWidth === 0 || img.naturalHeight === 0)) {
            console.log(`  ❌ Image failed to load (404 or server error)`);
        } else {
            console.log(`  ⏳ Image still loading...`);
        }
    });
};

window.forceCheckImages = () => {
    console.log('Force checking images without handler...');
    window.checkImages();
};
