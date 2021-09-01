from faker import Faker
import json            # To create a json file                 
import numpy as np

fake_data = Faker()

# class Hike:
#     """A hike."""

#     def __init__(self, hike_id, rating_id, location_id, name, zipcode, hike_length, dog_friendly, average_rating):
#         self.hike_id = hike_id
#         self.rating_id = rating_id
#         self.location_id = location_id
#         self.name = name
#         self.zipcode = zipcode
#         self.hike_length = hike_length
#         self.dog_friendly = dog_friendly
#         self.average_rating = average_rating

#     def __repr__self():
#         return 'name: {}, zipcode: {}, average_rating: {}'.format(self.name, self.zipcode, self.average_rating)

def create_data(x): 
  
    # dictionary 
    hike_data ={} 
    for i in range(0, x): 
        hike_data[i]={} 
        hike_data[i]['hike_id']= i
        hike_data[i]['rating_id']= np.random.randint(0,5) 
        hike_data[i]['location_id']= np.random.randint(0,5) 
        hike_data[i]['name']= fake_data.name()
        hike_data[i]['zipcode']= fake_data.zipcode()
        hike_data[i]['hike_length']= np.random.randint(0,5) 
        hike_data[i]['dog_friendly']= fake_data.boolean()
        hike_data[i]['average_rating (1-5)']= np.random.randint(0,5) 
    
    return hike_data
    
hikes = create_data(10)  # hikes dictionary