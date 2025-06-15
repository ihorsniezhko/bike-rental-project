from django.contrib import admin
# Import Profile model.
from .models import Profile

# Register the Profile model with the admin site.
# Lets view the extra info (like date of birth) associated with each user.
admin.site.register(Profile)
