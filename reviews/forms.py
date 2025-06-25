from django import forms
# Import Summernote to get a rich text editor.
from django_summernote.widgets import SummernoteWidget
# Import Review model to build the form.
from .models import Review


# ModelForm builds the form directly from Review model.
class ReviewForm(forms.ModelForm):
    """
    A form for creating and updating `Review` objects.

    **Fields:**
    - `rating`: The numerical rating from 1 to 5.
    - `comment`: The user's review comment, using a rich text editor.

    **Meta:**
    - `model`: The `Review` model.
    - `fields`: The fields to be included in the form.
    - `widgets`: Custom widgets for the form fields.
    """
    # Which model to use and fields to show.
    class Meta:
        # Form is for the Review model.
        model = Review
        # User set only rating and comment.
        fields = ['rating', 'comment']
        # Customize how fields are rendered.
        widgets = {
            # Use the rich text editor.
            'comment': SummernoteWidget(),
            # Use an HTML5 for the rating.
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
