document.addEventListener('DOMContentLoaded', function() {
    // Initialize all star rating forms on the page
    const ratingForms = document.querySelectorAll('.star-rating-form');
    
    ratingForms.forEach(form => {
        const stars = form.querySelectorAll('.star-rating input[type="radio"]');
        const ratingInput = form.querySelector('input[name="rating"]');
        const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
        const productId = form.dataset.productId;
        const url = form.action || '/rate-product/';
        
        // Set initial rating if it exists
        if (ratingInput && ratingInput.value) {
            const rating = parseInt(ratingInput.value);
            if (rating > 0) {
                const starToCheck = form.querySelector(`.star-rating input[value="${rating}"]`);
                if (starToCheck) starToCheck.checked = true;
            }
        }
        
        // Handle star click
        stars.forEach(star => {
            star.addEventListener('click', function() {
                const rating = this.value;
                
                // Update the hidden input
                if (ratingInput) {
                    ratingInput.value = rating;
                }
                
                // Send rating to server
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': csrfToken,
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: `product_id=${productId}&rating=${rating}`
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        // Optional: Show success message
                        console.log('Rating saved successfully');
                    }
                })
                .catch(error => {
                    console.error('Error saving rating:', error);
                });
            });
        });
    });
});
