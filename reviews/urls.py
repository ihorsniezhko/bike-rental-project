from django.urls import path
from . import views

urlpatterns = [
    # URL for editing a review (uses review primary key pk).
    path('edit/<int:pk>/', views.EditReview.as_view(), name='edit_review'),
    # URL for deleting a review (uses review primary key pk).
    path(
        'delete/<int:pk>/', views.DeleteReview.as_view(), name='delete_review'
        ),
]
