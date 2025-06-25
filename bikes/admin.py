from django.contrib import admin
# Import Bike model.
from .models import Bike
# Import SummernoteModelAdmin for rich text.
from django_summernote.admin import SummernoteModelAdmin


# Decorator to register a custom admin class
@admin.register(Bike)
class BikeAdmin(SummernoteModelAdmin):
    """
    Customizes the admin interface for the Bike model.

    **Admin Panel Features:**
    - Uses the Summernote editor for the `description` field
    for a rich text editing experience.

    **Inherits from:**
    - `django_summernote.admin.SummernoteModelAdmin`: Provides
    the Summernote widget for specified fields.
    """
    summernote_fields = ('description',)
