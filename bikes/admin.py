from django.contrib import admin
# Import Bike model.
from .models import Bike

# Register the Bike model.
# Create, view, update, and delete bike records.
admin.site.register(Bike)
