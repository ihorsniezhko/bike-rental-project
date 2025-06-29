from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from bikes.models import Bike
from reviews.models import Review


class ReviewModelTest(TestCase):
    """
    Tests for the Review model.
    """

    def setUp(self):
        """
        Set up non-modified objects used by all test methods.
        """
        self.user = User.objects.create_user(
            username='testuser', password='password'
        )
        self.bike = Bike.objects.create(
            name='Test Bike',
            type='Urban',
            price_per_hour=7.00
        )
        self.review = Review.objects.create(
            bike=self.bike,
            user=self.user,
            rating=4,
            comment="A good bike!"
        )

    def test_review_creation(self):
        """
        Test that a review can be created successfully.
        """
        self.assertEqual(self.review.bike.name, 'Test Bike')
        self.assertEqual(self.review.user.username, 'testuser')
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.comment, "A good bike!")
        self.assertEqual(Review.objects.count(), 1)

    def test_review_str_representation(self):
        """
        Test the string representation of the Review model.
        """
        expected_str = f"Review by {self.user.username} for {self.bike.name}"
        self.assertEqual(str(self.review), expected_str)

    def test_rating_validator_too_high(self):
        """
        Test that a rating above 5 raises a ValidationError.
        """
        review = Review(
            bike=self.bike, user=self.user, rating=6, comment="Too high"
        )
        # full_clean() is needed to run model validation
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_rating_validator_too_low(self):
        """
        Test that a rating below 1 raises a ValidationError.
        """
        review = Review(
            bike=self.bike, user=self.user, rating=0, comment="Too low"
        )
        with self.assertRaises(ValidationError):
            review.full_clean()


class DeleteReviewViewTest(TestCase):
    """
    Tests for the DeleteReview view.
    """

    def setUp(self):
        """
        Set up users, a bike, and a review for testing the view.
        """
        self.client = Client()
        self.owner = User.objects.create_user(
            username='owner', password='password'
        )
        self.bike = Bike.objects.create(
            name='Deletable Bike', type='Road', price_per_hour=15.00
        )
        self.review = Review.objects.create(
            bike=self.bike, user=self.owner, rating=5, comment="Delete me."
        )
        self.delete_url = reverse(
            'delete_review', kwargs={'pk': self.review.pk}
        )
        self.bike_detail_url = reverse(
            'bike_detail', kwargs={'pk': self.bike.pk}
        )

    def test_owner_can_delete_review(self):
        """
        Test that the author of a review can delete it.
        """
        self.client.login(username='owner', password='password')
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.bike_detail_url)
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())
