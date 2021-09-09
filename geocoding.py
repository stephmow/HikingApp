import requests
import os

API_KEY = os.environ['GOOGLE_API_KEY']



# https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=YOUR_API_KEY


latlng = '40.714224, -73.961452'
address = '311 Oak street, oakland, ca'

params = {
    'key': API_KEY, 
    'latlng': latlng
}

base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
response = requests.get(base_url, params = params).json()   
# response.keys()

# zipcode = response['results'][0]['address_components'][7]['long_name']
# print(zipcode)
zipcode = None

for item in response['results'][0]['address_components']:
    if item['types'][0] == 'postal_code':
        zipcode = item['long_name']

print(zipcode)

# {'address_components': 
#     [
#         {'long_name': '277', 'short_name': '277', 'types': ['street_number']}, 
#         {'long_name': 'Bedford Avenue', 'short_name': 'Bedford Ave', 'types': ['route']}, {'long_name': 'Williamsburg', 'short_name': 'Williamsburg', 'types': ['neighborhood', 'political']}, {'long_name': 'Brooklyn', 'short_name': 'Brooklyn', 'types': ['political', 'sublocality', 'sublocality_level_1']}, {'long_name': 'Kings County', 'short_name': 'Kings County', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'New York', 'short_name': 'NY', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United States', 'short_name': 'US', 'types': ['country', 'political']}, {'long_name': '11211', 'short_name': '11211', 'types': ['postal_code']}], 

#     'formatted_address': '277 Bedford Ave, Brooklyn, NY 11211, USA', 'geometry': {'location': {'lat': 40.7142205, 'lng': -73.9612903}, 'location_type': 'ROOFTOP', 'viewport': {'northeast': {'lat': 40.71556948029149, 'lng': -73.95994131970849}, 'southwest': {'lat': 40.7128715197085, 'lng': -73.9626392802915}}}, 'place_id': 'ChIJd8BlQ2BZwokRAFUEcm_qrcA', 'plus_code': {'compound_code': 'P27Q+MF Brooklyn, NY, USA', 'global_code': '87G8P27Q+MF'}, 'types': ['street_address']}