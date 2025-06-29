from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from bikes.models import Bike
from rentals.models import Rental


class CreateRentalViewTest(TestCase):
    """
    Tests for the create_rental view.
    """

    def setUp(self):
        """
        Set up a user and a bike for testing.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='renter', password='password'
        )
        self.available_bike = Bike.objects.create(
            name='Available Test Bike',
            type='Urban',
            price_per_hour=7.00,
            is_available=True
        )
        self.unavailable_bike = Bike.objects.create(
            name='Unavailable Test Bike',
            type='Urban',
            price_per_hour=7.00,
            is_available=False
        )
        self.create_rental_url = reverse(
            'create_rental', kwargs={'bike_id': self.available_bike.id}
        )
        # 'profile' is the name of the profile URL
        self.profile_url = reverse('profile')

    def test_authenticated_user_can_create_rental(self):
        """
        Test that a logged-in user can successfully rent an available bike.
        """
        self.client.login(username='renter', password='password')
        response = self.client.post(self.create_rental_url)

        self.assertRedirects(response, self.profile_url)
        self.assertTrue(Rental.objects.filter(
            user=self.user, bike=self.available_bike).exists())
        self.available_bike.refresh_from_db()
        self.assertFalse(self.available_bike.is_available)

    def test_user_with_active_rental_cannot_rent_another_bike(self):
        """
        Test that a user with an active rental cannot rent another bike.
        """
        # Create an initial active rental for user
        Rental.objects.create(user=self.user, bike=self.unavailable_bike)

        self.client.login(username='renter', password='password')
        response = self.client.post(self.create_rental_url)

        self.assertRedirects(response, self.profile_url)
        # Only the initial rental should exist
        self.assertEqual(Rental.objects.count(), 1)
