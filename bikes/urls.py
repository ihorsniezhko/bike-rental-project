from django.urls import path
from . import views

urlpatterns = [
    # Path '' represents homepage linked to BikeList view
    # Name 'home' for reference.
    path('', views.BikeList.as_view(), name='home'),
    # Dynamic path captures the bike primary key and passes to view.
    path('bike/<int:pk>/', views.BikeDetail.as_view(), name='bike_detail'),
]