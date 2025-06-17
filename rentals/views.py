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
    bike = get_object_or_404(Bike, id=bike_id)
    # User cannot rent more than one bike at a time.
    if Rental.objects.filter(user=request.user, end_time__isnull=True).exists():
        messages.error(request, "You already have an active rental.")
        return redirect('profile')
    # Check to ensure the bike is still available.
    if bike.is_available:
        # Create the new rental record.
        Rental.objects.create(user=request.user, bike=bike)
        # Update the bike's status to unavailable.
        bike.is_available = False
        bike.save()
        # Success message displayed.
        messages.success(request, f"You have successfully rented {bike.name}.")
        # Redirect to user's profile page.
        return redirect('profile')
    else:
        messages.error(request, "Sorry, this bike is no longer available.")
        return redirect('home')

@login_required
def return_bike(request, rental_id):
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
        messages.success(request, f"Thank you for returning {rental.bike.name}. Total cost: ${cost}.")
    else:
        messages.error(request, "This rental has already been completed.")
    return redirect('profile')