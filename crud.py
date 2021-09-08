"""CRUD operations."""

from model import db, User, Hike, Rating, Bookmark, connect_to_db

# Create functions 

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
    #User

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

    #Hikes 

def get_all_hikes():
    """Return all hikes"""

    return Hike.query.all()


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

def get_bookmark_coords(user_id):
    """Return json dict of all bookmarked hike coordinates"""

    bookmark_coord = db.session.query(Hike.latitude, Hike.longitude, Hike.hike_id).join(Bookmark).filter(Bookmark.user_id == user_id)

    bookmark_list =[]

    for item in bookmark_coord:
        bookmark_dict = {'lat' : item[0],
                        'lng' : item[1],
                        'hike_id' : item[2]}
        bookmark_list.append(bookmark_dict)

    return (bookmark_list)

def get_bookmark_coords(user_id):
    """Return json dict of all completed hike coordinates"""

    rating_coord = db.session.query(Hike.latitude, Hike.longitude, Hike.hike_id).join(Rating).filter(Rating.user_id == user_id)

    rating_list =[]

    for item in rating_coord:
        rating_dict = {'lat' : item[0],
                        'lng' : item[1],
                        'hike_id' : item[2]}
        rating_list.append(rating_dict)

    return (rating_list)



    # Bookmarks / Ratings

def get_bookmarks_obj_by_user_email(user_email):

    return Bookmark.query.filter(User.email == user_email)

def get_bookmarks_by_user_email(user_email):

    bookmarks = Bookmark.query.filter(User.email == user_email)
    bookmarks_list = []

    for bookmark in bookmarks: 
        bookmarks_dict = {'bookmark_id': bookmark.bookmark_id, 
                            'hike_id': bookmark.hike_id,
                            'is_completed': bookmark.is_completed }
        bookmarks_list.append(bookmarks_dict)

    return bookmarks_list


def check_bookmark(bookmark_id):

    return Bookmark.query.filter(Bookmark.bookmark_id == bookmark_id)    


def get_ratings_obj_by_user_email(user_email):

    return Rating.query.filter(User.email == user_email)

def get_ratings_by_user_email(user_email):

    ratings = Rating.query.filter(User.email == user_email)
    ratings_list = []

    for rating in ratings: 
        rating_dict = {'rating_id': rating.rating_id, 
                            'hike_id': rating.hike_id}
        ratings_list.append(rating_dict)

    return ratings_list



# def check_hike(user_id, hike_id):
    """Check if a hike is in the Bookmarks database"""
    # check if user_id and hike_id have a bookmark

    # Bookmark.query.filter(user_id = user_id)
    # if Bookmark.query.filter(User.user_id) == user_id and Bookmark.query.filter(hike_id)

    

# Delete functions
    # DELETE BOOKMARK  -- IF USER CREATES RATING (I.E. IS_COMPLETE == TRUE), THEN DELETE BOOKMARK
    # DELETE RATING



if __name__ == '__main__':
    from server import app
    connect_to_db(app)