from django.shortcuts import render
# Ggeneric views
from django.views import generic
# Handling URL reversals and user authentication
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
# Import Review model and ReviewForm
from .models import Review
from .forms import ReviewForm

class EditReview(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """
    A view to allow a logged-in user to edit their own review.
    """
    # Model and the form to use.
    model = Review
    form_class = ReviewForm
    # Template used to render the edit form.
    template_name = "reviews/edit_review.html"

    def test_func(self):
        """
        This function prevents one user from editing another user's review.
        It checks if the logged-in user is the author of the review.
        """
        review = self.get_object()
        return self.request.user == review.user

    def get_success_url(self):
        """
        Redirect the user back to the bike's detail page after editing.
        """
        # Bike associated with review.
        bike = self.object.bike
        # Success message.
        messages.success(self.request, 'Your review has been updated successfully.')
        # Return the URL for bike's detail page.
        return reverse_lazy('bike_detail', kwargs={'pk': bike.pk})


class DeleteReview(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """
    A view to allow a logged-in user to delete their own review.
    """
    model = Review
    template_name = "reviews/review_confirm_delete.html"
    # Redirect user back to the homepage after delete.
    success_url = reverse_lazy('home')

    def test_func(self):
        """
        This function prevents one user from deleting another user's review.
        """
        review = self.get_object()
        return self.request.user == review.user
    
    def delete(self, request, *args, **kwargs):
        """
        This method is called when the deletion is confirmed.
        Add a success message here.
        """
        messages.success(self.request, 'Your review has been deleted successfully.')
        return super(DeleteReview, self).delete(request, *args, **kwargs)

