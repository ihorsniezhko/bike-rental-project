from django.db import models
from cloudinary.models import CloudinaryField # For images on Cloudinary.
from django.db.models import Avg # Calculate the average rating.

# Defines the structure of the 'Bike' table.
class Bike(models.Model):
    # Simple text field for bike's name.
    name = models.CharField(max_length=100)
    # Text field for the bike's type.
    type = models.CharField(max_length=50)
    # Text field for the bike's size.
    size = models.CharField(max_length=10)
    # Boolean field to check if the bike is currently available.
    is_available = models.BooleanField(default=True)
    # Storing currency values.
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    # Field from Cloudinary for handling image uploads.
    featured_image = CloudinaryField('image', default='placeholder')

    # Property that calculates the average rating on the fly.
    @property
    def average_rating(self):
        # Gets all reviews related to this bike, and calculates the average of 'rating' field
        # If there are no reviews, it returns 0.
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Magic method useful for the Django admin panel and for debugging.
    def __str__(self):
        return self.name