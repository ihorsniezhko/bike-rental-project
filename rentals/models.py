from django.db import models
from django.contrib.auth.models import User
# Import Bike model from bikes app
from bikes.models import Bike


# Track each individual rental transaction.
class Rental(models.Model):
    """
    Represents a rental transaction.

    **Fields:**
    - `user`: A foreign key to the `User` who is renting the bike.
    - `bike`: A foreign key to the `Bike` being rented.
    - `start_time`: The timestamp when the rental period begins.
    - `end_time`: The timestamp when the rental period ends.
    - `total_cost`: The total cost of the rental.
    """
    # Many-to-one link to the User model. A user can have many rentals.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rentals"
        )
    # Many-to-one link to the Bike model. A bike can have many rentals.
    bike = models.ForeignKey(
        Bike, on_delete=models.CASCADE, related_name="rentals"
        )
    # Automatically record timestamp when a rental is created.
    start_time = models.DateTimeField(auto_now_add=True)
    # Timestamp for when the rental ends. Can be null because
    # an active rental hasn't ended yet.
    end_time = models.DateTimeField(null=True, blank=True)
    # Final cost of the rental (can be null until the rental is completed).
    total_cost = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
        )

    def __str__(self):
        """
        Returns the string representation of the Rental model.
        """
        return f"Rental {self.id} by {self.user.username}"
