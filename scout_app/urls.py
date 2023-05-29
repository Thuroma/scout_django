from django.urls import path
from . import views

urlpatterns = [
    path('', views.new_search, name='new_search'),
    path('search/<int:search_pk>', views.search_results, name='search_results'),
    path('bookmarked_searches', views.bookmarked_searches, name='bookmarked_searches'),
]