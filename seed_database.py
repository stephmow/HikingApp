"""Seed database with set of test data"""

import os
import json
import csv
from random import choice, randint 
import crud, model, server
import geocoder
import requests

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

os.system("dropdb hikedb") 
os.system("createdb hikedb")

model.connect_to_db(server.app)
model.db.create_all()

def seed_from_csv():
    with open ("hikedata.csv", "r") as f:
        reader = csv.reader(f)

        for row in reader:

            trail_id = row[0]
            name = row[1]
            city = row[3]
            location_id = row[6]
                # output: "\\{'lat': 20.71449, 'lng': -156.25085\\}"  which is a string
            location_strip = location_id.strip('\\{, \\}')
            location_split = location_strip.split()
                # output: ['lat':, 20.71449, , 'lng': , 156.25085]
            latitude = location_split[1].strip(",")
            longitude = location_split[3]

            # Geocode API Call for zipcode 
            latlng = latitude + ", " + longitude
            params = {
                        'key': GOOGLE_API_KEY, 
                        'latlng': latlng
                    }

            base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
            response = requests.get(base_url, params = params).json()   

            zipcode = None

            for item in response['results'][0]['address_components']:
                if item['types'][0] == 'postal_code':
                    zipcode = item['long_name']
         
            hike_length = float(row[8])
            difficulty = int(row[10])
            route_type = row[11]
            average_rating = float(row[13])
            activities = row[16]

        # example hike 
            # ['10011933', 
            # 'Puna Kau Trail', 
            # 'Hawaii Volcanoes National Park', 
            # 'Pahala', 
            # 'Hawaii', 
            # 'Hawaii', 
            # "\\{'lat': 19.29054, 'lng': -155.13412\\}", 6
            # '4.2363', 
            # '29289.988', 
            # '420.9288', 
            # '5', 10
            # 'out and back', 11
            # '', 
            # '4.5', 
            # '3', 
            # "['dogs-no', 'views']", "['hiking']", 
            # 'm\\']

            crud.create_hike(rating_id = None, location_id = None, city = city, latitude = latitude, longitude = longitude, zipcode = zipcode, name = name, hike_length = hike_length, average_rating = average_rating, difficulty = difficulty, route_type = route_type, activities = activities, dog_friendly = None)

    for n in range(10):
        email = f'user{n}@test.com'
        password = 'test'

        user = crud.create_user(email, password)

def seed_from_json():
    # Load (sample) hiking data from JSON file (from Yelp)
    with open('data.json') as f:
        hike_dict=json.loads(f.read())

    hikes_list = hike_dict['businesses']


    # Create hikes, store them in list so we can use them
    # to create fake ratings later
    hikes_in_db = []

    for hike in hikes_list:
        # get the name, rating and location in the hike list
        name = hike['name']
        rating = hike['rating']
        zipcode = hike['location']['zip_code']
        if 'dog' in hike['categories']:
            dog_friendly = True
        else:
            dog_friendly = False

        # create a hike here and append it to hikes_in_db
        new_hike = crud.create_hike(name, zipcode, rating)
        hikes_in_db.append(new_hike)


    for n in range(10):
        email = f'user{n}@test.com'
        password = 'test'

        # create a user here
        user = crud.create_user(email, password)

        for _ in range(10):
            random_hike = choice(hikes_in_db)
            rating = randint(1, 5)

            crud.create_rating(user, random_hike, rating)

if __name__ == "__main__":
    # seed_from_json()   change if using .json data 
    seed_from_csv()