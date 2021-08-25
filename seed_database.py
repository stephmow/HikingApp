"""Seed database with set of test data"""

import os
import json
from random import choice, randint 
# from datetime import datetime 
import crud, model, server

os.system('dropdb hikedb') 
os.system('createdb hikedb')

model.connect_to_db(server.app)
model.db.create_all()


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
        random_movie = choice(hikes_in_db)
        rating = randint(1, 5)

        crud.create_rating(user, random_movie, rating)

