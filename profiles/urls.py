from django.urls import path
from . import views

urlpatterns = [
    # Map the URL '/profile/' to profile_view function.
    path('', views.profile_view, name='profile'),
]
