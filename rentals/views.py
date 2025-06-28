from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# Import messages framework to show feedback.
from django.contrib import messages
# Import timezone to get the current time.
from django.utils import timezone
from .models import Rental
from bikes.models import Bike


@login_required
def create_rental(request, bike_id):
    """
    Creates a new rental for a bike.

    **Args:**
    - `request`: The HTTP request object.
    - `bike_id`: The ID of the bike to be rented.

    **Returns:**
    - A redirect to the user's profile page.
    """
    bike = get_object_or_404(Bike, id=bike_id)
    # User cannot rent more than one bike at a time.
    has_active_rental = Rental.objects.filter(
        user=request.user, end_time__isnull=True
    ).exists()
    if has_active_rental:
        messages.error(request, "You already have an active rental.")
        return redirect('profile')
    # Check to ensure the bike is still available.
    if bike.is_available:
        # Create the new rental record and capture it to use its properties.
        new_rental = Rental.objects.create(user=request.user, bike=bike)
        # Update bike status to unavailable.
        bike.is_available = False
        bike.save()
        # Format the start time for a user-friendly message.
        start_time_formatted = new_rental.start_time.strftime("%H:%M on %B %d")
        # Create a detailed success message.
        success_message = (
            f"You have successfully rented '{bike.name}'. "
            f"Your ride started at {start_time_formatted}. Enjoy!"
        )

        # Success message displayed.
        messages.success(request, success_message)
        # Redirect to user profile page.
        return redirect('profile')
    else:
        messages.error(request, "Sorry, this bike is no longer available.")
        return redirect('home')


@login_required
def return_bike(request, rental_id):
    """
    Handles the return of a rented bike.

    **Args:**
    - `request`: The HTTP request object.
    - `rental_id`: The ID of the rental being completed.

    **Returns:**
    - A redirect to the user's profile page.
    """
    # Get the specific rental object, ensuring it belongs to the current user.
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)
    # Check if the rental is still active.
    if rental.end_time is None:
        # Set the end time to now.
        rental.end_time = timezone.now()
        # Duration of the rental.
        duration = rental.end_time - rental.start_time
        # Hours rounding up to the next full hour.
        hours = int(duration.total_seconds() // 3600) + 1
        # Rental final cost.
        cost = hours * rental.bike.price_per_hour
        rental.total_cost = cost
        # Make the bike available again.
        rental.bike.is_available = True
        rental.bike.save()
        # Save the changes to rental object.
        rental.save()
        # The confirmation message.
        success_message = (
            f"Thank you for returning {rental.bike.name}. "
            f"Total cost: €{cost:.2f}."
        )
        messages.success(request, success_message)
    else:
        messages.error(request, "This rental has already been completed.")
    return redirect('profile')
