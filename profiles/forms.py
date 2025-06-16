from django import forms
from datetime import date

# Custom form inherits from django.forms.Form
class CustomSignupForm(forms.Form):
    # Add custom field.
    date_of_birth = forms.DateField(
        # Widget to render custom field, date picker in browsers.
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date of Birth",
        # Custom field is mandatory
        required=True
    )

    # Special Django method to run custom validation for specific field.
    def clean_date_of_birth(self):
        # Get the date of birth from the form cleaned data.
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            # Calculate age.
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            # Validation logic.
            if not 14 <= age <= 90:
                # If the age is outside the valid range, raise a ValidationError,
                # and display the message for the user.
                raise forms.ValidationError("You must be between 14 and 90 years old to register.")
        # Return the cleaned data.
        return dob

    # Signup method save 'user' object when we save custom field.
    def signup(self, request, user):
        # Save date_of_birth in user's profile.
        user.profile.date_of_birth = self.cleaned_data.get('date_of_birth')
        user.profile.save()