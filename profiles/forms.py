from django import forms
# To calculate the user's age.
from datetime import date


# Custom form inherits from django.forms.Form
class CustomSignupForm(forms.Form):
    """
    A custom form for user signup that includes additional fields
    for first name, last name, and date of birth.

    **Fields:**
    - `first_name`: The user's first name.
    - `last_name`: The user's last name.
    - `date_of_birth`: The user's date of birth.

    **Validation:**
    - Ensures that the user is between 14 and 90 years old.
    """
    # Mandatory First Name field.
    first_name = forms.CharField(
        max_length=30, label='First Name', required=True
    )
    # Mandatory Last Name field.
    last_name = forms.CharField(
        max_length=30, label='Last Name', required=True
    )

    # Add custom field.
    date_of_birth = forms.DateField(
        # Widget to render custom mandatory field (placeholder).
        widget=forms.DateInput(
            attrs={'type': 'text', 'placeholder': 'dd/mm/yyyy'}
            ),
        label="Date of Birth",
        help_text="Please use the format DD/MM/YYYY.",
        required=True)

    # Special Django method to run custom validation for specific field.
    def clean_date_of_birth(self):
        """
        Validates the date of birth to ensure the user is within
        the allowed age range.

        **Raises:**
        - `forms.ValidationError`: If the user's age is not between 14 and 90.

        **Returns:**
        - The cleaned date of birth.
        """
        # Get the date of birth from the form cleaned data.
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            # Calculate age.
            age = (
                today.year - dob.year -
                ((today.month, today.day) < (dob.month, dob.day))
            )
            # Validation logic.
            if not 14 <= age <= 90:
                error_message = (
                    "You must be between 14 and 90 years old to register."
                )
                raise forms.ValidationError(error_message)
        # Return cleaned data.
        return dob

    # Signup method save 'user' object when we save custom fields.
    def signup(self, request, user):
        """
        Saves the custom data from the form to the user and their profile.

        **Args:**
        - `request`: The HTTP request object.
        - `user`: The user object to be updated.

        **Returns:**
        - The updated user object.
        """
        # Add our custom data to the user object.
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()

        # Save the date of birth to profile model.
        user.profile.date_of_birth = self.cleaned_data.get('date_of_birth')
        user.profile.save()

        # Return the user object.
        return user