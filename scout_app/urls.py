from django.urls import path
from . import views

urlpatterns = [
    # home page
    path('', views.new_search, name='new_search'),

    # passing the search object from the search to the search results
    path('search/<int:search_pk>', views.search_results, name='search_results'),

    # passing the lat long map output to be searched
    path('search/', views.lat_long_search, name='lat_long_search'),

    # list of bookmarked searches
    path('bookmarked_searches', views.bookmarked_searches, name='bookmarked_searches'),
]