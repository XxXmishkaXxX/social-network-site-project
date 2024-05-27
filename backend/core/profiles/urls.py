from django.urls import path, re_path
from .views import (UserProfileCreate, GetCitiesByCountry, GetCountriesView, UserProfileWallView,
UserProfileEditAPIView, UserProfileShortDataView,)



urlpatterns = [
    path('create/', UserProfileCreate.as_view(), name='create-profile'),
    path('get_countries/', GetCountriesView.as_view(), name='get_countries'),
    path('get_cities_by_country/<int:id>/', GetCitiesByCountry.as_view(), name='get_cities_by_country'),
    path('wall/<int:pk>/', UserProfileWallView.as_view(), name='user-profile-wall'),
    path('edit/', UserProfileEditAPIView.as_view(), name='profile-edit'),
    path('short/<int:pk>/', UserProfileShortDataView.as_view(), name="short-data")
]