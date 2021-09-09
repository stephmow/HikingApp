import requests

url = "https://trailapi-trailapi.p.rapidapi.com/"

querystring = {"q-activities_activity_type_name_eq":"hiking","q-state_cont":"California"}

headers = {
    'x-rapidapi-host': "trailapi-trailapi.p.rapidapi.com",
    'x-rapidapi-key': RAPID_API_KEY
    }

response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text) 

data = response.json() # convert to json string to a dictionary

for item in data['places']:   # places is the only key
    print("Name: ", item['name'])
    print("City: ", item['city'])

"""
{'city': 'Adelaide', 
'state': None, 
'country': 'Australia', 
'name': 'Mount Lofty', 
'parent_id': None, 
'unique_id': 25908, 
'directions': 'This system  has several trails with different trail-heads on the South East Free-way, or near Waterfall Gully. From the city drive along Glen Osmond Road or Green Hill Road. Depending on the trail, the drive is 10 to 20 km.', 
'lat': -34.95096, 
'lon': 138.67247, 
'description': None, 
'date_created': None, 
'children': [], 
'activities': [{'name': 'Mount Lofty', 'unique_id': '1-8362', 'place_id': 25908, 'activity_type_id': 5, 'activity_type_name': 'mountain biking', 'url': 'http://www.singletracks.com/item.php?c=1&i=8362', 'attribs': {'"length"': '"50"', '"nightride"': 'null'}, 'description': 'Chambers Gully is single track that will take you to Cleland Conservation Park and then by road to Mt Lofty. Eagle Mountain Bike Park is a system of advanced loops.', 'length': 50, 'activity_type': {'created_at': '2012-08-15T16:12:35Z', 'id': 5, 'name': 'mountain biking', 'updated_at': '2012-08-15T16:12:35Z'}, 'thumbnail': None, 'rank': None, 'rating': 0}]}
"""