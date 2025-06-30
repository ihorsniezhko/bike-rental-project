/**
 * @jest-environment jsdom
 */

// This helper function creates the HTML for our star component in the test environment
const setupHTML = (initialValue = '') => {
  document.body.innerHTML = `
    <div class="star-rating">
      <input type="hidden" name="rating" value="${initialValue}">
      <span class="star" data-value="1"></span>
      <span class="star" data-value="2"></span>
      <span class="star" data-value="3"></span>
      <span class="star" data-value="4"></span>
      <span class="star" data-value="5"></span>
    </div>
  `;
};

describe('Star Rating Component', () => {
  // This function runs before each individual 'test' in this block.
  // It ensures each test starts with a clean slate.
  beforeEach(() => {
    // Reset modules to ensure our script's event listener is re-attached for each test
    jest.resetModules();
    // Set up the default HTML (with no initial rating)
    setupHTML();

    // Load the script. This attaches the 'DOMContentLoaded' event listener.
    require('./star-rating.js');

    // Manually trigger the 'DOMContentLoaded' event to run the script's main logic.
    document.dispatchEvent(new Event('DOMContentLoaded'));
  });

  describe('Initialization', () => {
    test('should not have any stars selected when initialized with no value', () => {
      const selectedStars = document.querySelectorAll('.star.selected');
      expect(selectedStars.length).toBe(0);
    });

    test('should have the correct number of stars selected when initialized with a value', () => {
      // For this specific test, we need to re-run the setup with an initial value.
      jest.resetModules();
      setupHTML('3'); // Initialize with a rating of 3
      require('./star-rating.js');
      document.dispatchEvent(new Event('DOMContentLoaded'));

      const selectedStars = document.querySelectorAll('.star.selected');
      expect(selectedStars.length).toBe(3);
      expect(document.querySelector('[data-value="3"]')).toHaveClass('selected');
      expect(document.querySelector('[data-value="4"]')).not.toHaveClass('selected');
    });
  });

  describe('User Interaction', () => {
    test('clicking a star should update the hidden input value', () => {
      const ratingInput = document.querySelector('input[type="hidden"]');
      const thirdStar = document.querySelector('.star[data-value="3"]');

      thirdStar.click();

      expect(ratingInput.value).toBe('3');
    });

    test('clicking a star should add the "selected" class to the correct stars', () => {
      const fourthStar = document.querySelector('.star[data-value="4"]');
      fourthStar.click();

      const selectedStars = document.querySelectorAll('.star.selected');
      expect(selectedStars.length).toBe(4);
      expect(document.querySelector('[data-value="4"]')).toHaveClass('selected');
      expect(document.querySelector('[data-value="5"]')).not.toHaveClass('selected');
    });

    test('hovering over a star should temporarily highlight it', () => {
      const fifthStar = document.querySelector('.star[data-value="5"]');
      
      // Simulate a 'mouseover' event
      const mouseoverEvent = new MouseEvent('mouseover', { bubbles: true });
      fifthStar.dispatchEvent(mouseoverEvent);

      const selectedStars = document.querySelectorAll('.star.selected');
      expect(selectedStars.length).toBe(5);
    });

    test('moving the mouse away should revert the highlight to the clicked value', () => {
      const secondStar = document.querySelector('.star[data-value="2"]');
      const fourthStar = document.querySelector('.star[data-value="4"]');
      
      // 1. Click the second star
      secondStar.click();
      expect(document.querySelectorAll('.star.selected').length).toBe(2);

      // 2. Hover over the fourth star
      const mouseoverEvent = new MouseEvent('mouseover', { bubbles: true });
      fourthStar.dispatchEvent(mouseoverEvent);
      expect(document.querySelectorAll('.star.selected').length).toBe(4);

      // 3. Move the mouse away
      const mouseoutEvent = new MouseEvent('mouseout', { bubbles: true });
      fourthStar.dispatchEvent(mouseoutEvent);

      // The selection should revert to the clicked value (2)
      expect(document.querySelectorAll('.star.selected').length).toBe(2);
    });
  });
});