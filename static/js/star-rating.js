document.addEventListener('DOMContentLoaded', function () {
    // Select all star rating containers
    const starContainers = document.querySelectorAll('.star-rating');

    starContainers.forEach(container => {
        // Find the hidden rating input and the stars within this container
        const ratingInput = container.querySelector('input[type="hidden"]');
        const stars = container.querySelectorAll('.star');

        // Function to set the visual state of the stars
        function setRating(value) {
            stars.forEach(star => {
                // Get the value of the current star from its data attribute
                const starValue = parseInt(star.dataset.value, 10);
                // Add 'selected' class if star's value is less than or equal to rating
                if (starValue <= value) {
                    star.classList.add('selected');
                } else {
                    star.classList.remove('selected');
                }
            });
        }

        // Add click event listener to each star
        stars.forEach(star => {
            star.addEventListener('click', function () {
                const value = this.dataset.value;
                // Update the hidden input field's value
                ratingInput.value = value;
                // Update the visual appearance of stars
                setRating(value);
            });

            // Add mouseover and mouseout events for a hover effect
            star.addEventListener('mouseover', function () {
                setRating(this.dataset.value);
            });

            star.addEventListener('mouseout', function () {
                // On mouseout reset the stars to the currently selected rating
                setRating(ratingInput.value);
            });
        });

        // Initialize the stars based on the input current value (if any)
        if (ratingInput.value) {
            setRating(ratingInput.value);
        }
    });
});
