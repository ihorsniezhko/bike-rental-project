from django.db import models
# For images on Cloudinary.
from cloudinary.models import CloudinaryField
# Calculate the average rating.
from django.db.models import Avg


# Defines the structure of the 'Bike' table.
class Bike(models.Model):
    """
    Represents a bike available for rent.

    **Fields:**
    - `name`: The name of the bike.
    - `type`: The type of the bike (e.g., Mountain, Road, Hybrid).
    - `description`: A detailed description of the bike.
    - `size`: The size of the bike.
    - `is_available`: A boolean indicating if the bike is
    currently available for rent.
    - `price_per_hour`: The cost to rent the bike for one hour.
    - `featured_image`: The main image of the bike, hosted on Cloudinary.

    **Properties:**
    - `average_rating`: Calculates and returns the average
    rating for the bike based on its reviews.
    """
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    size = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    featured_image = CloudinaryField('image', default='placeholder')

    # Property that calculates the average rating on the fly.
    @property
    def average_rating(self):
        """
        Calculates the average rating for the bike.

        **Returns:**
        - The average rating as a float, or 0 if there are no ratings.
        """
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    def __str__(self):
        """
        Returns the string representation of the Bike model.
        """
        return self.name
