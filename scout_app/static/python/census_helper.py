import requests
import os
from pprint import pprint
import urllib


census_api_key = os.getenv('CENSUS_KEY')


def get_geocoder_response_from_address(street_address, city, state):
    # layers at https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Current/MapServer
    # returns all layers
    address_geocoder_url = f'https://geocoding.geo.census.gov/geocoder/geographies/address'
    address_geocoder_query = {'street': street_address, 'city': city, 'state': state, 'benchmark': 'Public_AR_Census2020', 'vintage': 'Census2020_Census2020', 'layers': 'all', 'format': 'json'}
    address_geocoder_response = requests.get(address_geocoder_url, params=address_geocoder_query)
    addr_geocoder_response_json = address_geocoder_response.json()
    return addr_geocoder_response_json



def get_geocoder_response_from_lat_long(latitude, longitude):
    # layers at https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Current/MapServer
    # returns all layers
    coordinates_geocoder_url = 'https://geocoding.geo.census.gov/geocoder/geographies/coordinates'
    coordinates_geocoder_query = {'x': longitude, 'y': latitude, 'benchmark': 'Public_AR_Census2020', 'vintage': 'Census2020_Census2020', 'layers': 'all', 'format': 'json'}
    coordinates_geocoder_response = requests.get(coordinates_geocoder_url, params=coordinates_geocoder_query)
    coordinates_geocoder_response.raise_for_status()
    coordinates_geocoder_json = coordinates_geocoder_response.json()
    return coordinates_geocoder_json


def get_coordinates_from_address_geocoder_response(response):
    try:
        response_latitude = response['result']['addressMatches'][0]['coordinates']['y']
        response_longitude = response['result']['addressMatches'][0]['coordinates']['x']
        return response_latitude, response_longitude
    except IndexError as e:
        print('There was an error getting the coordinates from the geocoder.')
        

def get_geo_codes_from_address_geocoder_response(response):

    geography_data_names_and_codes = {}

    if  'Census Blocks' in response['result']['addressMatches'][0]['geographies']:
        block_code = response['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['BLOCK']
        tract_code = response['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['TRACT']
        state_code = response['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['STATE']
        county_code = response['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['COUNTY']

        geography_data_names_and_codes['block'] = f'{block_code}'        
        geography_data_names_and_codes['tract'] = f'{tract_code}'
        geography_data_names_and_codes['state_code'] = f'{state_code}'
        geography_data_names_and_codes['county_code'] = f'{county_code}'

    if  'Counties' in response['result']['addressMatches'][0]['geographies']:
        county_name = response['result']['addressMatches'][0]['geographies']['Counties'][0]['NAME']
        geography_data_names_and_codes['county_name'] = f'{county_name}'

    if  'States' in response['result']['addressMatches'][0]['geographies']:
        state_name = response['result']['addressMatches'][0]['geographies']['States'][0]['BASENAME']
        geography_data_names_and_codes['state_name'] = f'{state_name}'

    if  'County Subdivisions' in response['result']['addressMatches'][0]['geographies']:
        county_subdivision_name = response['result']['addressMatches'][0]['geographies']['County Subdivisions'][0]['BASENAME']
        county_subdivision_code = response['result']['addressMatches'][0]['geographies']['County Subdivisions'][0]['COUSUB']

        geography_data_names_and_codes['county_subdivision_name'] = f'{county_subdivision_name}'
        geography_data_names_and_codes['county_subdivision_code'] = f'{county_subdivision_code}'

    if  'Incorporated Places' in response['result']['addressMatches'][0]['geographies']:
        incorporated_place_name = response['result']['addressMatches'][0]['geographies']['Incorporated Places'][0]['BASENAME']
        incorporated_place_code = response['result']['addressMatches'][0]['geographies']['Incorporated Places'][0]['PLACE']

        geography_data_names_and_codes['incorporated_place_name'] = f'{incorporated_place_name}'
        geography_data_names_and_codes['incorporated_place_code'] = f'{incorporated_place_code}'

    if  'Unified School Districts' in response['result']['addressMatches'][0]['geographies']:
        school_district_name = response['result']['addressMatches'][0]['geographies']['Unified School Districts'][0]['BASENAME']
        school_district_code = response['result']['addressMatches'][0]['geographies']['Unified School Districts'][0]['SDUNI']

        geography_data_names_and_codes['school_district_name'] = f'{school_district_name}'
        geography_data_names_and_codes['school_district_code'] = f'{school_district_code}'

    return geography_data_names_and_codes


def get_geo_codes_from_coordinate_geocoder_response(response):

    geography_data_names_and_codes = {}

    if  'Census Blocks' in response['result']['geographies']:
        block_code = response['result']['geographies']['Census Blocks'][0]['BLOCK']
        tract_code = response['result']['geographies']['Census Blocks'][0]['TRACT']
        state_code = response['result']['geographies']['Census Blocks'][0]['STATE']
        county_code = response['result']['geographies']['Census Blocks'][0]['COUNTY']

        geography_data_names_and_codes['block'] = f'{block_code}'        
        geography_data_names_and_codes['tract'] = f'{tract_code}'
        geography_data_names_and_codes['state_code'] = f'{state_code}'
        geography_data_names_and_codes['county_code'] = f'{county_code}'


    if 'Counties' in response['result']['geographies']:
        county_name = response['result']['geographies']['Counties'][0]['NAME']
        geography_data_names_and_codes['county_name'] = f'{county_name}'

    if  'States' in response['result']['geographies']:
        state_name = response['result']['geographies']['States'][0]['BASENAME']
        geography_data_names_and_codes['state_name'] = f'{state_name}'
    
    if  'County Subdivisions' in response['result']['geographies']:
        county_subdivision_name = response['result']['geographies']['County Subdivisions'][0]['BASENAME']
        county_subdivision_code = response['result']['geographies']['County Subdivisions'][0]['COUSUB']

        geography_data_names_and_codes['county_subdivision_name'] = f'{county_subdivision_name}'
        geography_data_names_and_codes['county_subdivision_code'] = f'{county_subdivision_code}'

    if  'Incorporated Places' in response['result']['geographies']:
        incorporated_place_name = response['result']['geographies']['Incorporated Places'][0]['BASENAME']
        incorporated_place_code = response['result']['geographies']['Incorporated Places'][0]['PLACE']

        geography_data_names_and_codes['incorporated_place_name'] = f'{incorporated_place_name}'
        geography_data_names_and_codes['incorporated_place_code'] = f'{incorporated_place_code}'

    if  'Unified School Districts' in response['result']['geographies']:
        school_district_name = response['result']['geographies']['Unified School Districts'][0]['BASENAME']
        school_district_code = response['result']['geographies']['Unified School Districts'][0]['SDUNI']

        geography_data_names_and_codes['school_district_name'] = f'{school_district_name}'
        geography_data_names_and_codes['school_district_code'] = f'{school_district_code}'

    return geography_data_names_and_codes
    


def get_census_acs_response(search_geography_data):

    """
    These are the items in the query list

    'B01001_001E' : "POPULATION ESTIMATE TOTAL"
    'B06011_001E' : "Estimate!!Median income in the past 12 months --!!Total:"
    'B14006_002E' : "Estimate!!Total:!!Individuals with income in the past 12 months below the poverty level:"
    'B15002_002E' : 'Estimate!!Total:!!Male: Total over the age of 25'
    'B15002_011E' : 'Estimate!!Total:!!Male:!!High school graduate (includes equivalency)'
    'B15002_014E' : "Estimate!!Total:!!Male:!!Associate's degree"
    'B15002_015E' : "Estimate!!Total:!!Male:!!Bachelor's degree"
    'B15002_016E' : "Estimate!!Total:!!Male:!!Master's degree"
    'B15002_017E' : 'Estimate!!Total:!!Male:!!Professional school degree'
    'B15002_018E' : 'Estimate!!Total:!!Male:!!Doctorate degree'
    'B15002_019E' : 'Estimate!!Total:!!Female: Total over the age of 25'
    'B15002_028E' : 'Estimate!!Total:!!Female:!!High school graduate (includes equivalency)'
    'B15002_031E' : "Estimate!!Total:!!Female:!!Associate's degree"
    'B15002_032E' : "Estimate!!Total:!!Female:!!Bachelor's degree"
    'B15002_033E' : "Estimate!!Total:!!Female:!!Master's degree"
    'B15002_034E' : 'Estimate!!Total:!!Female:!!Professional school degree'
    'B15002_035E' : 'Estimate!!Total:!!Female:!!Doctorate degree'
    """
        

    census_acs_url = 'https://api.census.gov/data/2021/acs/acs5?'
    
    query_list = ['NAME','B01001_001E','B06011_001E', 'B14006_002E','B15002_002E','B15002_011E','B15002_014E','B15002_015E','B15002_016E','B15002_017E','B15002_018E','B15002_019E','B15002_028E','B15002_031E','B15002_032E','B15002_033E','B15002_034E','B15002_035E']

    if 'county_code' in search_geography_data:
        payload = {
            'get': ','.join(query_list),
            'for': f'county:{search_geography_data["county_code"]}',
            'in': f'state:{search_geography_data["state_code"]}'
        }

    if 'county_subdivision_code' in search_geography_data:
        payload = {
            'get': ','.join(query_list),
            'for': f'county%20subdivision:{search_geography_data["county_subdivision_code"]}',
            'in': f'state:{search_geography_data["state_code"]}%20county:{search_geography_data["county_code"]}'
        }
        
    if 'incorporated_place_code' in search_geography_data:
        payload = {
            'get': ','.join(query_list),
            'for': f'place:{search_geography_data["incorporated_place_code"]}',
            'in': f'state:{search_geography_data["state_code"]}'
        }  

    payload_query = urllib.parse.urlencode(payload, safe=':+,%')
    census_acs_response = requests.get(census_acs_url, params=payload_query)
    census_acs_response.raise_for_status()
    census_acs_response_json = census_acs_response.json()
    return census_acs_response_json


def sort_acs_data(acs_response_data):
    acs_population_data = {
        'title': 'Population data',
        'data': [
            {'variable': 'B01001_001E', 'label': 'Total population', 'value': ''},
        ]
    }

    acs_income_data = {
        'title': 'Income data',
        'data': [
            {'variable': 'B06011_001E', 'label': "Median income in the past 12 months", 'value': ''},
            {'variable': 'B14006_002E', 'label': "Individuals with annual income below the poverty level", 'value': ''},
        ]
    }

    acs_education_male_data = {
        'title': 'Education attainment for males over 25',
        'data': [
            {'variable': 'B15002_002E', 'label': 'Total over the age of 25', 'value': ''},
            {'variable': 'B15002_011E', 'label': 'High school graduate (includes equivalency)', 'value': ''},
            {'variable': 'B15002_014E', 'label': "Associate's degree", 'value': ''},
            {'variable': 'B15002_015E', 'label': "Bachelor's degree", 'value': ''},
            {'variable': 'B15002_016E', 'label': "Master's degree", 'value': ''},
            {'variable': 'B15002_017E', 'label': 'Professional school degree', 'value': ''},
            {'variable': 'B15002_018E', 'label': 'Doctorate degree', 'value': ''},
        ]
    }

    acs_education_female_data = {
        'title': 'Education attainment for females over 25',
        'data': [
            {'variable': 'B15002_019E', 'label': 'Total over the age of 25', 'value': ''},
            {'variable': 'B15002_028E', 'label': 'High school graduate (includes equivalency)', 'value': ''},
            {'variable': 'B15002_031E', 'label': "Associate's degree", 'value': ''},
            {'variable': 'B15002_032E', 'label': "Bachelor's degree", 'value': ''},
            {'variable': 'B15002_033E', 'label': "Master's degree", 'value': ''},
            {'variable': 'B15002_034E', 'label': 'Professional school degree', 'value': ''},
            {'variable': 'B15002_035E', 'label': 'Doctorate degree', 'value': ''}
        ]
    }

    acs_variable_list = acs_response_data[0]
    acs_value_list = acs_response_data[1]
    acs_variable_value_dictionary = dict(zip(acs_variable_list, acs_value_list))

    for variable in acs_variable_value_dictionary:

        for data in acs_population_data['data']:
            if variable == data['variable']:
                data['value'] = acs_variable_value_dictionary[variable]

        for data in acs_income_data['data']:
            if variable == data['variable']:
                data['value'] = acs_variable_value_dictionary[variable]

        for data in acs_education_male_data['data']:
            if variable == data['variable']:
                data['value'] = acs_variable_value_dictionary[variable]

        for data in acs_education_female_data['data']:
            if variable == data['variable']:
                data['value'] = acs_variable_value_dictionary[variable]
            
        
    census_display_data = [acs_population_data, acs_income_data, acs_education_male_data, acs_education_female_data]          

    return census_display_data


