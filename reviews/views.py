# Generic views
from django.views import generic
# Handling URL reversals and user authentication
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.contrib import messages
# Import Review model and ReviewForm
from .models import Review
from .forms import ReviewForm


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
        review = self.get_object()
        return self.request.user == review.user

    def get_success_url(self):
        """
        Returns the URL to redirect to after a successful review update.

        **Returns:**
        - The URL of the bike's detail page.
        """
        # Bike associated with review.
        bike = self.object.bike
        # Success message.
        messages.success(
            self.request, 'Your review has been updated successfully.'
            )
        # Return the URL for bike's detail page.
        return reverse_lazy('bike_detail', kwargs={'pk': bike.pk})


class DeleteReview(
        LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """
    Allows a logged-in user to delete their own review.

    **Mixins:**
    - `LoginRequiredMixin`: Ensures that only authenticated users
    can access this view.
    - `UserPassesTestMixin`: Ensures that the user deleting the review
    is the author of the review.

    **Template:**
    - `reviews/review_confirm_delete.html`
    """
    model = Review
    template_name = "reviews/review_confirm_delete.html"
    # Redirect user back to the homepage after delete.
    success_url = reverse_lazy('home')

    def test_func(self):
        """
        Checks if the current user is the author of the review.

        **Returns:**
        - `True` if the user is the author, `False` otherwise.
        """
        review = self.get_object()
        return self.request.user == review.user

    def delete(self, request, *args, **kwargs):
        """
        Handles the deletion of the review and adds a success message.

        **Args:**
        - `request`: The HTTP request object.
        - `*args`, `**kwargs`: Additional arguments.

        **Returns:**
        - An `HttpResponseRedirect` to the `success_url`.
        """
        messages.success(
            self.request, 'Your review has been deleted successfully.'
            )
        return super().delete(request, *args, **kwargs)
