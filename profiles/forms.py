from django import forms
# To calculate the user's age.
from datetime import date

# Custom form inherits from django.forms.Form
class CustomSignupForm(forms.Form):
    # Mandatory First Name field.
    first_name = forms.CharField(max_length=30, label='First Name', required=True)
    # Mandatory Last Name field.
    last_name = forms.CharField(max_length=30, label='Last Name', required=True)
    
    # Add custom field.
    date_of_birth = forms.DateField(
        # Widget to render custom mandatory field, placeholder tells which format to use.
        widget=forms.DateInput(attrs={'type': 'text', 'placeholder': 'dd/mm/yyyy'}),
        label="Date of Birth", required=True)

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

    # Signup method save 'user' object when we save custom fields.
    def signup(self, request, user):
        """
        Custom signup logic to save extra fields.
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