from django.urls import path, re_path
from .views import UserProfileCreate, GetCitiesByCountry, GetCountriesView, UserProfileView, UserProfileEditAPIView



urlpatterns = [
    path('create/', UserProfileCreate.as_view(), name='create-profile'),
    path('get_countries/', GetCountriesView.as_view(), name='get_countries'),
    path('get_cities_by_country/<int:id>/', GetCitiesByCountry.as_view(), name='get_cities_by_country'),
    path('<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('edit/<int:pk>/', UserProfileEditAPIView.as_view(), name='profile-edit')
]