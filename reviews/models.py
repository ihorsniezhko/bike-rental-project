from django.db import models
from django.contrib.auth.models import User
from bikes.models import Bike
# Import validators to enforce rules on model fields.
from django.core.validators import MinValueValidator, MaxValueValidator


# Stores user reviews for bikes.
class Review(models.Model):
    """
    Represents a user review for a bike.

    **Fields:**
    - `bike`: A foreign key to the `Bike` that is being reviewed.
    - `user`: A foreign key to the `User` who wrote the review.
    - `rating`: An integer rating from 1 to 5.
    - `comment`: The text of the review.
    - `created_at`: The timestamp when the review was created.
    """
    # Link to the Bike that being reviewed.
    bike = models.ForeignKey(
        Bike, on_delete=models.CASCADE, related_name="reviews"
        )
    # Link to the User who did review.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
        )
    # Integer field for the rating.
    # Ensure that the number entered is between 1 and 5.
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
        )
    # Large text field for the review comment.
    comment = models.TextField()
    # Timestamp is automatically set when the review is created.
    created_at = models.DateTimeField(auto_now_add=True)

    # Meta class provides additional options for the model.
    class Meta:
        # Whenever we get a list of reviews, they are ordered
        # by the newest first.
        ordering = ["-created_at"]

    def __str__(self):
        """
        Returns the string representation of the Review model.
        """
        return f"Review by {self.user.username} for {self.bike.name}"
