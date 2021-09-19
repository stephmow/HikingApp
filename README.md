# Take A Hike!

A web application that allows users to search for hiking trails by name, zipcode or city and displays information for the hike.  Logged in users can create a list of saved and/or completed hikes.

### Features with Screenshots

- Create an account and login
- Search for hikes by name, city and/or zipcode
![login](/static/images/login.jpg)
- See list of hiking trails within search criteria
![results](/static/images/results.jpg)
- See details on selected hike, including ratings, difficulty, activities and location on google maps
- Get directions to selected hike
- Save, rate and comment on hikes
![details](/static/images/details.jpg)
- Refer to bookmarked hikes on a single map on homepage
- Delete saved and/or completed hike bookmarks 
![homepage](/static/images/homepage.jpg)

### Tech Stack Used

- Backend: Python, PostgreSQL
- Frontend: JavaScript, jQuery, HTML, CSS, Bootstrap
- APIs Used: Google Maps and Geocoding API
- Other: Unsplash for background image

### Installation

Clone github repository to your terminal:

```sh
git clone https://github.com/stephmow/TakeAHike
```
Set up and activate your virtual environment:
```sh
python3 -m venv env
```

```sh
source env/bin/activate
```

Install project dependencies: 
```sh
pip3 install -r requirements.txt
```
Sign up for a Google API key and save it to a secrets.sh file in the project folder.  Refer to: [Google Maps Developer Tools - Create API Key](https://developers.google.com/maps/documentation/javascript/get-api-key)

Source the secrets.sh file

```sh
source secrets.sh
```

Create a hike database. Since all hike contents have been saved to 'hike_revised.sql', dump the contents into your newly created hike database. 

```sh
createdb hikedb
```

```sh
psql hikedb < hike_revised.sql
```

Run the server.py file:
```sh
python3 server.py
```

Go to your browser and type in 'localhost:5000'.  