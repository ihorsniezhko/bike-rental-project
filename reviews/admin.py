from django.contrib import admin
from .models import Review
# Import SummernoteModelAdmin to get the rich text editor in the admin panel.
from django_summernote.admin import SummernoteModelAdmin

# Decorator to register a model.
@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):
    """
    Customizes the admin interface for the Revie model
    to use the Summernote editor.
    """
    # Apply Summernote editor to the 'comment' field.
    summernote_fields = ('comment',)