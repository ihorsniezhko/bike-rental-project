from django.contrib import admin
# Import Bike model.
from .models import Bike
# Import SummernoteModelAdmin for rich text.
from django_summernote.admin import SummernoteModelAdmin

# Decorator to register a custom admin class
@admin.register(Bike)
class BikeAdmin(SummernoteModelAdmin):
    """
    Customizes the admin interface for the Bike model
    to use the Summernote editor for the description field.
    """
    # Apply Summernote editor to the 'comment' field.
    summernote_fields = ('description',)

