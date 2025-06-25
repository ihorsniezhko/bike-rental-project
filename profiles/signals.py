# Import the necessary modules
from django.db.models.signals import post_save
# Sender model
from django.contrib.auth.models import User
# Decorator to receive the signal
from django.dispatch import receiver
# Model to create
from .models import Profile


# The @receiver decorator connects this function to a signal.
# Run this function after post_save
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Creates a Profile object automatically whenever a new User is created.

    **Args:**
    - `sender`: The model class that sent the signal (User).
    - `instance`: The actual instance being saved.
    - `created`: A boolean; True if a new record was created.
    - `**kwargs`: Wildcard keyword arguments.
    """
    if created:
        Profile.objects.create(user=instance)


# Save profile when user object is saved.
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Saves the Profile object automatically whenever the associated
    User object is saved.

    **Args:**
    - `sender`: The model class that sent the signal (User).
    - `instance`: The actual instance being saved.
    - `**kwargs`: Wildcard keyword arguments.
    """
    instance.profile.save()
