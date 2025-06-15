from django.db import models
from django.contrib.auth.models import User
from bikes.models import Bike # Import Bike model from bikes app

# Track each individual rental transaction.
class Rental(models.Model):
    # Many-to-one link to the User model. A user can have many rentals.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rentals")
    # Many-to-one link to the Bike model. A bike can have many rentals.
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name="rentals")
    # Automatically record timestamp when a rental is created.
    start_time = models.DateTimeField(auto_now_add=True)
    # Timestamp for when the rental ends. Can be null because
    # an active rental hasn't ended yet.
    end_time = models.DateTimeField(null=True, blank=True)
    # Final cost of the rental (can be null until the rental is completed).
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    # String representation for a Rental object.
    def __str__(self):
        return f"Rental {self.id} by {self.user.username}"