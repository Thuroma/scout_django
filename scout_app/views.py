import requests
import logging
import os
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Search
from .forms import NewSearchForm
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()



@login_required
def new_search(request):

    """ This is the main page.
        Displays the map and a search form for address input.
        """
    
    if request.method == 'POST':
        new_search_form = NewSearchForm(request.POST)
        search = new_search_form.save(commit=False)     # Create a new Place from the form
        search.user = request.user                      # Associate the search with the logged in user

        one_line_to_lat_long_url = 'https://geocoding.geo.census.gov/geocoder/locations/address'
        geocoder_address_to_lat_long_query = {'street': search.street_address, 'city': search.city, 'state': search.state, 'zip': search.zip_code, 'benchmark': '2020', 'format': 'json'}
        geocoder_address_to_lat_long_response = requests.get(one_line_to_lat_long_url, params=geocoder_address_to_lat_long_query)
        geocoder_address_to_lat_long_json = geocoder_address_to_lat_long_response.json()

        search.latitude = geocoder_address_to_lat_long_json["result"]["addressMatches"][0]["coordinates"]["y"]
        search.longitude = geocoder_address_to_lat_long_json["result"]["addressMatches"][0]["coordinates"]["x"]

        if new_search_form.is_valid():                  # Checks against DB constraints, for example, are required fields present?
            search.save()                               # Saves to the database
            return redirect('search_results', search_pk=search.pk)
        print('Not valid.')


    new_search_form = NewSearchForm()
    return render(request, 'scout_app/search.html', { 'new_search_form': new_search_form })


@login_required
def lat_long_search(request):

    """ 
    Perform a search using the map click event
    """

    print(request.POST)
    
    if request.method == 'POST':
        new_search_form = NewSearchForm(request.POST)
        print(new_search_form)
        if new_search_form.is_valid():                  # Checks against DB constraints, for example, are required fields present?
        # search = new_search_form.save(commit=False)     # Create a new Search from the form
            search = Search()
            search.user = request.user                      # Associate the search with the logged in user
            search.latitude = request.POST['latitude']
            search.longitude = request.POST['longitude']
            search.save()                               # Saves to the database
            return redirect('search_results', search_pk=search.pk)
        print('Not valid.')


    new_search_form = NewSearchForm()
    return render(request, 'scout_app/search.html', { 'new_search_form': new_search_form })
    

@login_required
def search_results(request, search_pk):

    """ This will take the coordinates from the new_search_form
        make a call to the geocoder
        pass the results to the apis
        then display the search_results.html page 
        """
        
    search = get_object_or_404(Search, pk=search_pk)

    try:

        # full url for lat/long to geo codes - results in lat/long coordinates
        # https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x=-93.86762&y=45.39167&benchmark=Public_AR_Census2020&vintage=Census2020_Census2020&layers=26,80,82&format=json
        
        # save the url for the geocoder - lat/long to geographies
        geocoder_coordinates_to_geographies_url = 'https://geocoding.geo.census.gov/geocoder/geographies/coordinates'
        # save the params
        geocoder_coordinates_to_geographies_query = {'x': search.longitude, 'y': search.latitude, 'benchmark': 'Public_AR_Census2020', 'vintage': 'Census2020_Census2020', 'layers': '26,80,82', 'format': 'json'}

        # send the response to the search results page

        geocoder_geography_response = requests.get(geocoder_coordinates_to_geographies_url, params=geocoder_coordinates_to_geographies_query)
        geocoder_geography_response_json = geocoder_geography_response.json()

        # extract the county and state codes from the geocoder response
        county_level_geo_id = geocoder_geography_response_json['result']['geographies']['Counties'][0]['GEOID']
        county_level_state_code = county_level_geo_id[0:2]
        county_level_county_code = county_level_geo_id[2:5]

        # get the census data
        census_api_key = os.getenv('CENSUS_KEY')
        county_census_api_url = f'https://api.census.gov/data/2020/dec/pl?get=NAME,P1_001N,P1_003N,P1_004N,P1_005N,P1_006N,P1_007N,P2_002N,P5_002N,P5_003N,P5_004N,P5_008N,P5_009N&for=county:{county_level_county_code}&in=state:{county_level_state_code}&key={census_api_key}'

        # Use the state and county codes to make the census api call
        county_census_response = requests.get(county_census_api_url)
        county_census_response.raise_for_status()
        county_census_response_json = county_census_response.json()

        # # extract the census data from the response
        county_name = county_census_response_json[1][0]
        county_total_population = county_census_response_json[1][1]
        county_white_population = county_census_response_json[1][2]
        county_black_population = county_census_response_json[1][3]
        county_indigenous_population = county_census_response_json[1][4]
        county_asian_population = county_census_response_json[1][5]
        county_pacific_population = county_census_response_json[1][6]
        county_hispanic_population = county_census_response_json[1][7]
        county_institutionalized_population = county_census_response_json[1][8]
        county_institutionalized_adult_population = county_census_response_json[1][9]
        county_institutionalized_juvenile = county_census_response_json[1][10]
        county_university_student_housing_population = county_census_response_json[1][11]
        county_military_quarters = county_census_response_json[1][12]

        # calculate percentages for race populations
        county_white_percentage = round(((int(county_white_population) / int(county_total_population)) * 100), 2)
        county_black_percentage = round(((int(county_black_population) / int(county_total_population)) * 100), 2)
        county_indigenous_percentage = round(((int(county_indigenous_population) / int(county_total_population)) * 100), 2)
        county_asian_percentage = round(((int(county_asian_population) / int(county_total_population)) * 100), 2)
        county_pacific_percentage = round(((int(county_pacific_population) / int(county_total_population)) * 100), 2)
        county_hispanic_percentage = round(((int(county_hispanic_population) / int(county_total_population)) * 100), 2)

    except KeyError as e:
        print('There was an issue with the census call.' + e)


    try:
        # YELP SECTION
        # 1609.3 meters per mile
        search_miles = 2
        search_radius = search_miles * 1609
        search_limit = 5

        yelp_api_authorization = os.getenv('YELP_AUTHORIZATION')

        headers = {
            "accept": "application/json",
            "Authorization": f'{yelp_api_authorization}'
        }

        list_of_keywords = ['Park', 'Civic Center', 'Fitness', 'Brewery', 'Restaurant', 'Grocery Store', 'School', 'Convienience Stores', 'Bars', 'Vegan']

        yelp_results_dictionary = {}

        for keyword in list_of_keywords:
            
            url = f'https://api.yelp.com/v3/businesses/search?latitude={search.latitude}&longitude={search.longitude}&term={keyword}&radius={search_radius}&categories=&sort_by=best_match&limit={search_limit}'

            response = requests.get(url, headers=headers)
            response_json = response.json()

            if response_json['businesses'] != []:
                yelp_results_dictionary[f'{keyword}'] = response_json

    except:
        print('There was an issue with the yelp call.')

    context = { 
        'latitude': search.latitude, 
        'longitude': search.longitude,
        'name': county_name,
        'total_pop': county_total_population,
        'white_pop': county_white_percentage,
        'black_pop': county_black_percentage,
        'indigenous_pop': county_indigenous_percentage,
        'asian_pop': county_asian_percentage,
        'pacific_pop': county_pacific_percentage,
        'hispanic_pop': county_hispanic_percentage,
        'institutionalized_pop': county_institutionalized_population,
        'institutionalized_adult': county_institutionalized_adult_population,
        'institutionalized_juvenile': county_institutionalized_juvenile,
        'university_housing': county_university_student_housing_population,
        'military_pop': county_military_quarters,
        'yelp_data': yelp_results_dictionary }

    return render(request, 'scout_app/search_results.html', context)



    
    
@login_required
def bookmarked_searches(request):

    """ If this is a POST request, the user clicked the Scout button
        in the form. Check if the new search is valid, if so, save a 
        new Search to the database, and redirect to this same page.
        This creates a GET request to this same route.
        
        If not a POST route, or Search is not valid, display a page with
        a list of searches and a form to sdd a new search.
        """

    searches = Search.objects.filter(user=request.user).order_by('name')
    return render(request, 'scout_app/bookmarked_searches.html', { 'searches': searches })
