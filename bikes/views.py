# Import necessary modules.
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View, generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Import models and forms.
from .models import Bike
from reviews.models import Review
from reviews.forms import ReviewForm

# View inherits Django ListView.
class BikeList(generic.ListView):
    """
    A view to display a list of all available bikes.
    """
    # Which model to use.
    model = Bike
    # Only get available bikes (filtered set).
    queryset = Bike.objects.filter(is_available=True).order_by('type')
    # Specify the view template file.
    template_name = 'index.html'
    # Variable that hold the list of bikes in the template.
    context_object_name = 'bike_list'

# Standard view to handle GET and POST requests (view page, submit review)
class BikeDetail(View):
    """
    A view to handle the detail page for a single bike.
    """
    # GET method called when user navigates to the URL.
    def get(self, request, *args, **kwargs):
        # Primary key passed from the URL.
        pk = kwargs.get('pk')
        # If the bike doesn't exist, show 404 Not Found page.
        bike = get_object_or_404(Bike, pk=pk)
        # Get all reviews associated with this bike.
        reviews = bike.reviews.all()

        # Empty ReviewForm instance to render form on the page.
        review_form = ReviewForm()

        # Request, template file, context data to pass to the template.
        return render(
            request,
            "bike_detail.html",
            {
                "bike": bike,
                "reviews": reviews,
                "review_form": review_form,
            },
        )