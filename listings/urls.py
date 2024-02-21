from django.urls import path

from listings.views.cities import CityListView, CityView
from listings.views.getCities import CityDistrictsView
from listings.views.getListings import Filter, ListingDetailView, ListingView
from listings.views.getSubjects import GetSubjects
from listings.views.manageListings import ManageListing

urlpatterns = [
    path('ManageListing', ManageListing.as_view()),
    path('getListingsForMainPage', ListingView.as_view()),
    path('cities', CityListView.as_view()),
    path('', Filter.as_view()),

    path('get_cities_with_districts', CityDistrictsView.as_view()),

    path('get_specific_listing', ListingDetailView.as_view()),
    path('get_subjects', GetSubjects.as_view()),

    path('cities/<int:city_id>', CityView.as_view()),
    path('<int:pk>', Filter.as_view())
]
