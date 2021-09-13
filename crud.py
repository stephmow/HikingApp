"""CRUD operations."""

from model import db, User, Hike, Rating, Bookmark, connect_to_db

# Create Functions 

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()
    
    print(f"Successfully added student: {email}")

    return user


def create_hike(rating_id, location_id, city, latitude, longitude, zipcode, name, hike_length, average_rating, difficulty, route_type, activities, dog_friendly):
    """Create and return a new hike."""

    hike = Hike(rating_id = rating_id, location_id = location_id, city = city, latitude = latitude, longitude = longitude, zipcode = zipcode, name = name, hike_length = hike_length, average_rating=average_rating, difficulty = difficulty, route_type = route_type, activities = activities, dog_friendly = dog_friendly)

    db.session.add(hike)
    db.session.commit()

    return hike


def create_bookmark(user, hike, is_completed):  
    """Create a bookmark for a hike"""

    hike_bookmark = Bookmark(user=user, hike=hike, is_completed = is_completed)

    db.session.add(hike_bookmark)
    db.session.commit()

    return hike_bookmark


def create_rating(user, hike, rating, comments=''):  
    """Create a rating with User instance and Hike instance"""

    hike_rating = Rating(user=user, hike=hike, rating=rating, comments=comments)

    db.session.add(hike_rating)
    db.session.commit()

    return hike_rating


# Retrieve functions 

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def get_all_hikes():
    """Return all hikes"""

    return Hike.query.all()


def get_hike_search():
    """Return all relevant search info from hike db"""

    hikes = Hike.query.all()
    hike_search = []

    for hike in hikes: 
        if hike.name not in hike_search:
            hike_search.append(hike.name)
        if hike.city not in hike_search:
            hike_search.append(hike.city)
        if hike.zipcode is not None and hike.zipcode not in hike_search: 
            hike_search.append(str(hike.zipcode))

    return hike_search


def get_hikes_by_zip():
    """Given a zipcode, provide list of nearby hikes"""

    return Hike.query.all()


def get_hike_details(hike_id):
    """Provide hike details including photo, length, etc."""

    return Hike.query.get(hike_id)


def get_hike_coords(hike_id):
    """Return json dict of hike coordinates"""

    hike = get_hike_details(hike_id)
    lat = float(hike.latitude)  #convert from string to float
    lng = float(hike.longitude)

    return {'lat': lat, 'lng': lng}


def get_bookmarks_by_user_id(user_id):

    return Bookmark.query.filter(Bookmark.user_id == user_id).all()


def get_bookmarks_by_user_email(user_email):

    bookmarks = Bookmark.query.filter(User.email == user_email).all()
    bookmarks_list = []

    for bookmark in bookmarks: 
        bookmarks_dict = {'bookmark_id': bookmark.bookmark_id, 
                            'hike_id': bookmark.hike_id,
                            'is_completed': bookmark.is_completed }
        bookmarks_list.append(bookmarks_dict)

    return bookmarks_list


def get_bookmark_coords(user_id):
    """Return json dict of all bookmarked hike coordinates"""

    bookmark_coord = db.session.query(Hike.latitude, Hike.longitude, Hike.hike_id).join(Bookmark).filter(Bookmark.user_id == user_id).all()

    bookmark_list =[]

    for item in bookmark_coord:
        bookmark_dict = {'lat' : item[0],
                        'lng' : item[1],
                        'hike_id' : str(item[2])}
        print(bookmark_dict)
        bookmark_list.append(bookmark_dict)

    return (bookmark_list)


def get_ratings_by_user_id(user_id):

    return Rating.query.filter(Rating.user_id == user_id).all()


def get_ratings_by_user_email(user_email):

    ratings = Rating.query.filter(User.email == user_email).all()
    ratings_list = []

    for rating in ratings: 
        rating_dict = {'rating_id': rating.rating_id, 
                            'hike_id': rating.hike_id}
        ratings_list.append(rating_dict)

    return ratings_list


def get_rating_coords(user_id):
    """Return json dict of all completed hike coordinates"""

    rating_coord = db.session.query(Hike.latitude, Hike.longitude, Hike.hike_id).join(Rating).filter(Rating.user_id == user_id).all()

    rating_list =[]

    for item in rating_coord:
        rating_dict = {'lat' : item[0],
                        'lng' : item[1],
                        'hike_id' : item[2]}
        rating_list.append(rating_dict)

    return (rating_list)

    
# Delete functions

def delete_bookmark(user, hike_id):  
    """Delete a bookmark for a hike"""

    hike_bookmark = Bookmark.query.filter(Bookmark.user == user, Bookmark.hike_id == hike_id).one()
    
    db.session.delete(hike_bookmark)
    db.session.commit()

    return hike_bookmark


def delete_rating(user, hike_id):  
    """Delete a rating for a hike"""

    hike_rating = Rating.query.filter(Rating.user == user, Rating.hike_id == hike_id).one()
    
    db.session.delete(hike_rating)
    db.session.commit()

    return hike_rating


if __name__ == '__main__':
    from server import app
    connect_to_db(app)