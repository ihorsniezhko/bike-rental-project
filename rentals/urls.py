from django.urls import path
from . import views

urlpatterns = [
    # URL for creating a rental (uses bike_id).
    path('create/<int:bike_id>/', views.create_rental, name='create_rental'),
    # URL for returning a bike (uses rental_id).
    path('return/<int:rental_id>/', views.return_bike, name='return_bike'),
]