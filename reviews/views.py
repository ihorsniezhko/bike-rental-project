# Generic views
from django.views import generic, View
# Handling URL reversals and user authentication
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.contrib import messages
# Import Review model and ReviewForm
from .models import Review
from .forms import ReviewForm
from django.shortcuts import get_object_or_404, redirect


class EditReview(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """
    Allows a logged-in user to edit their own review.

    **Mixins:**
    - `LoginRequiredMixin`: Ensures that only authenticated users
      can access this view.
    - `UserPassesTestMixin`: Ensures that the user editing the review
      is the author of the review.

    **Template:**
    - `reviews/edit_review.html`
    """
    # Model and the form to use.
    model = Review
    form_class = ReviewForm
    # Template used to render the edit form.
    template_name = "reviews/edit_review.html"

    def test_func(self):
        """
        Checks if the current user is the author of the review.

        **Returns:**
        - `True` if the user is the author, `False` otherwise.
        """
        # Get the review object that is being edited.
        review = self.get_object()
        # Check if the logged-in user is the same as the user who did review.
        return self.request.user == review.user

    def get_success_url(self):
        """
        Returns the URL to redirect to after a successful review update.

        **Returns:**
        - The URL of the bike's detail page.
        """
        # Get the bike associated with the review that was just updated.
        bike = self.object.bike
        # Create a success message to be displayed on the next page.
        messages.success(
            self.request, 'Your review has been updated successfully.'
            )
        # Return the URL for the associated bike's detail page.
        return reverse_lazy('bike_detail', kwargs={'pk': bike.pk})


class DeleteReview(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Handles the deletion of a review via a POST request,
    without confirmation.

    **Mixins:**
    - `LoginRequiredMixin`: Ensures that only authenticated users can
      perform this action.
    - `UserPassesTestMixin`: Ensures that only the author of the review
      can delete it.
    """
    def post(self, request, *args, **kwargs):
        """
        Handles the POST request to delete a review.

        **Args:**
        - `request`: The HTTP request object. `*args`, `**kwargs`: Additional
        arguments, including the review's primary key (`pk`).
        **Returns:** An `HttpResponseRedirect` to the bike's
        detail page.
        """
        # Retrieve the specific review to be deleted.
        review = get_object_or_404(
            Review, pk=kwargs['pk'], user=request.user
            )
        # Store the primary key of bike before deleting the review.
        bike_pk = review.bike.pk
        # Delete review object from the database.
        review.delete()
        # Create a success message for the user.
        messages.success(request, 'Your review has been successfully deleted.')
        # Redirect the user back to the bike detail page.
        return redirect('bike_detail', pk=bike_pk)

    def test_func(self):
        """
        Checks if the current user is the author of the review before
        allowing the POST request.

        **Returns:**
        - `True` if the user is the author, `False` otherwise.
        """
        # Get the review object based on primary key from the URL.
        review = get_object_or_404(Review, pk=self.kwargs['pk'])
        # Verify that logged-in user is the review author.
        return self.request.user == review.user
