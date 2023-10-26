import requests
import logging
import os
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Search
from .forms import NewSearchForm
from pprint import pprint
from dotenv import load_dotenv
from .static.python.census_helper import *

load_dotenv()


def new_search(request):

    """ This is the main page.
        Displays the map and a search form for address input.
        """
    
    if request.method == 'POST':
        new_search_form = NewSearchForm(request.POST)
        if new_search_form.is_valid():                  # Checks against DB constraints, for example, are required fields present?

            street_address = request.POST['street_address']
            city = request.POST['city']
            state = request.POST['state']

            geocoder_response_from_address_search = get_geocoder_response_from_address(street_address, city, state)

            coordinates_from_address_search = get_coordinates_from_address_geocoder_response(geocoder_response_from_address_search)
            try:
                latitude = coordinates_from_address_search[0]
                longitude = coordinates_from_address_search[1]
            except TypeError as e:
                messages.info(request, 'Please use the map for this search')
                return render(request, 'scout_app/search.html', { 'new_search_form': new_search_form })

            return redirect('search_results', latitude=latitude, longitude=longitude )
        print('Not valid.')

    new_search_form = NewSearchForm()
    return render(request, 'scout_app/search.html', { 'new_search_form': new_search_form })


def lat_long_search(request):

    """ 
    Perform a search using the map click event
    """
    
    if request.method == 'POST':
        new_search_form = NewSearchForm(request.POST)
        if new_search_form.is_valid():                  # Checks against DB constraints, for example, are required fields present?
            latitude = request.POST['latitude']
            longitude = request.POST['longitude']

            return redirect('search_results', latitude=latitude, longitude=longitude )
        print('Not valid.')

    new_search_form = NewSearchForm()
    return render(request, 'scout_app/search.html', { 'new_search_form': new_search_form })
    

def search_results(request, latitude, longitude):

    """ This will take the coordinates from the new_search_form
        make a call to the geocoder
        pass the results to the apis
        then display the search_results.html page 
        """

    try:      

        geography_response_from_lat_long = get_geocoder_response_from_lat_long(latitude, longitude)

        census_geography_data = get_geo_codes_from_coordinate_geocoder_response(geography_response_from_lat_long)

        acs_data = get_census_acs_response(census_geography_data)

        census_acs_display_data = sort_acs_data(acs_data)

    except KeyError as e:
        print('There was an issue with the census call.')


    try:
        # YELP SECTION
        # Orange - #FF8100
        # Green - #00831E
        # Teal - #008BB0
        # Red - #AD0606
        # Purple - #7F00B0
        # Blue - #0009C5
        # Pink - #FF00E3


        # 1609.3 meters per mile
        search_miles = 5
        search_radius = search_miles * 1609
        search_limit = 10

        yelp_api_authorization = os.getenv('YELP_AUTHORIZATION')

        headers = {
            "accept": "application/json",
            "Authorization": f'{yelp_api_authorization}'
        }

        yelp_display_data = [
            {'category': 'Parks', 
             'image_url': 'park_map_icon.png'},
            {'category': 'Civic Centers', 
             'image_url': 'civic_center_map_icon.png'},
            {'category': 'Gyms', 
             'image_url': 'gym_map_icon.png'},
            {'category': 'Breweries', 
             'image_url': 'brewery_map_icon.png'},
            {'category': 'Restaurants', 
             'image_url': 'restaurant_map_icon.png'},
            {'category': 'Grocery Stores', 
             'image_url': 'market_map_icon.png'},
            {'category': 'Gas Stations', 
             'image_url': 'gas_station_map_icon.png'},
            {'category': 'Convienience Stores', 
             'image_url': 'shop_map_icon.png'},
            {'category': 'Bars', 
             'image_url': 'bar_map_icon.png'},
            {'category': 'Vegan', 
             'image_url': 'vegan_map_icon.png'},
            
        ]

        for search_term in yelp_display_data:

            category = search_term['category']
            
            url = f'https://api.yelp.com/v3/businesses/search?latitude={latitude}&longitude={longitude}&term={category}&radius={search_radius}&categories=&sort_by=best_match&limit={search_limit}'

            response = requests.get(url, headers=headers)
            response_json = response.json()

            search_term['data'] = response_json['businesses']

    except KeyError as e:
        print('There was an issue with the yelp call.' + e)

    context = { 
        'latitude': latitude,
        'longitude': longitude,
        'census_geography_data': census_geography_data,
        'census_acs_display_data': census_acs_display_data,
        'yelp_display_data': yelp_display_data }

    return render(request, 'scout_app/search_results.html', context)
