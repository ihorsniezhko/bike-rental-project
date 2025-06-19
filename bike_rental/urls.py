"""
URL configuration for bike_rental project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # Add include


urlpatterns = [
    path('admin/', admin.site.urls),
    # Includes all necessary authentication URLs.
    path("accounts/", include("allauth.urls")),
    # Include bikes URLs.
    path('', include('bikes.urls')),
    # Include Profile URLs
    path('profile/', include('profiles.urls')),
    # Include Rentals URLs
    path('rental/', include('rentals.urls')),
    # Include Summernote URLs
    path('summernote/', include('django_summernote.urls')),
]
