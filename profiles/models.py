from django.db import models
# Import Django built-in User model
from django.contrib.auth.models import User


# Extends the built-in User model with additional fields.
class Profile(models.Model):
    """
    Extends the default Django User model to include additional
    user information.

    **Fields:**
    - `user`: A one-to-one relationship with the User model.
    - `date_of_birth`: The user's date of birth.
    """
    # One-to-one link (if a User is deleted, their Profile is deleted too).
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # To store the user's date of birth, can be empty.
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        """
        Returns the string representation of the Profile model.
        """
        return f'{self.user.username} Profile'
