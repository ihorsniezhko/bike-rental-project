# Import necessary modules.
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View, generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Import Avg to calculate the average rating at the database level.
from django.db.models import Avg

# Import models and forms.
from .models import Bike
from reviews.forms import ReviewForm


# View inherits Django ListView.
class BikeList(generic.ListView):
    """
    Displays a list of available bikes, with sorting options.

    **Context:**
    - `bike_list`: A queryset of `Bike` objects where `is_available` is True.

    **Template:**
    - `index.html`
    """
    # Which model to use.
    model = Bike
    # Specify the view template file.
    template_name = 'index.html'
    # Variable that holds the list of bikes in the template.
    context_object_name = 'bike_list'

    def get_queryset(self):
        """
        Returns the list of available bikes,
        optionally sorted by a user-selected parameter.
        Optimized to perform sorting at the database level.
        """
        queryset = Bike.objects.filter(is_available=True)
        # Get the sorting parameter from the URL, default 'name_asc'.
        sort_by = self.request.GET.get('sort_by', 'name_asc')

        # A dictionary to map the sort_by parameter to ordering field.
        ordering_map = {
            'name_asc': 'name',
            'name_desc': '-name',
            'type_asc': 'type',
            'type_desc': '-type',
            'price_asc': 'price_per_hour',
            'price_desc': '-price_per_hour',
            # Special handling for size and rating.
        }

        if sort_by in ordering_map:
            queryset = queryset.order_by(ordering_map[sort_by])

        # Handling for size (allow for custom or numeric sorting).
        elif sort_by == 'size_asc':
            queryset = queryset.order_by('size')
        elif sort_by == 'size_desc':
            queryset = queryset.order_by('-size')

        # Handling for rating (annotate method to calculate average rating).
        elif sort_by == 'rating_asc':
            queryset = queryset.annotate(
                avg_rating=Avg('reviews__rating')
            ).order_by('avg_rating')
        elif sort_by == 'rating_desc':
            queryset = queryset.annotate(
                avg_rating=Avg('reviews__rating')
            ).order_by('-avg_rating')

        # Default sort if invalid parameter
        else:
            queryset = queryset.order_by('name')

        return queryset


# Standard view to handle GET and POST requests (view page, submit review)
class BikeDetail(View):
    """
    Displays the details of a single bike and handles review submissions.

    **GET:**
    - Renders the bike detail page with the bike's information
    and a form to submit a review.

    **POST:**
    - Handles the submission of a new review for the bike.
    """
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests for the bike detail page.

        **Args:**
        - `request`: The HTTP request object.
        - `*args`, `**kwargs`: Additional arguments, including
        the primary key (`pk`) of the bike.

        **Returns:**
        - An `HttpResponse` object that renders
        the `bike_detail.html` template.
        """
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

    # Decorator ensures only logged-in users can post reviews.
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for submitting a review.

        **Args:**
        - `request`: The HTTP request object.
        - `*args`, `**kwargs`: Additional arguments, including
        the primary key (`pk`) of the bike.

        **Returns:**
        - A redirect to the bike detail page if the form is valid.
        - An `HttpResponse` object that re-renders the `bike_detail.html`
        template with form errors if the form is invalid.
        """
        pk = kwargs.get('pk')
        bike = get_object_or_404(Bike, pk=pk)

        # Create form with POST data from the request.
        review_form = ReviewForm(data=request.POST)

        # Built-in form validation.
        if review_form.is_valid():
            # Set user for the review before saving.
            review_form.instance.user = request.user
            # Only create the review object.
            review = review_form.save(commit=False)
            # Associate the review with the correct bike.
            review.bike = bike
            # Save created review object to the database.
            review.save()
            messages.success(request, "Review submitted successfully!")
            # Redirect to bike detail page to see the review.
            return redirect('bike_detail', pk=bike.pk)
        else:
            # If form contains error, re-render page and display error message.
            reviews = bike.reviews.all()
            messages.error(request, "There was an error with your submission.")
            return render(
                request,
                "bike_detail.html",
                {
                    "bike": bike,
                    "reviews": reviews,
                    # Pass form with errors
                    "review_form": review_form,
                },
            )
