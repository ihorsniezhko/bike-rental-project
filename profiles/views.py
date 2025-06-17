from django.shortcuts import render
# Ensure that only logged-in users can access view.
from django.contrib.auth.decorators import login_required
from rentals.models import Rental

@login_required
def profile_view(request):
    # Get active rentals for the current user (end_time is null).
    active_rentals = Rental.objects.filter(user=request.user, end_time__isnull=True)
    # Get returned rentals for the current user (end_time is NOT null).
    # Order by the most recently returned first.
    past_rentals = Rental.objects.filter(user=request.user, end_time__isnull=False).order_by('-end_time')

    # Pass rental querysets to the template.
    context = {
        'active_rentals': active_rentals,
        'past_rentals': past_rentals,
    }
    return render(request, 'profiles/profile.html', context)