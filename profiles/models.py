from django.db import models
from django.contrib.auth.models import User # Import Django built-in User model

# Extends the built-in User model with additional fields.
class Profile(models.Model):
    # One-to-one link between a Profile and a User (if a User is deleted, their Profile is deleted too).
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # To store the user's date of birth, can be empty.
    date_of_birth = models.DateField(null=True, blank=True)

    # String representation for a Profile object.
    def __str__(self):
        return f'{self.user.username} Profile'