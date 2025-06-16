# Import the necessary modules
from django.db.models.signals import post_save
from django.contrib.auth.models import User # Sender model
from django.dispatch import receiver # Decorator to receive the signal
from .models import Profile # Model to create

# The @receiver decorator connects this function to a signal.
# Run this function after post_save
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # Variable 'created' is True if a new record created.
    # Create a profile for newly created users only.
    if created:
        Profile.objects.create(user=instance)

# Save profile when user object is saved.
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()