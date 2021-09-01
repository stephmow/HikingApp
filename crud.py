"""CRUD operations."""

from model import db, User, Hike, Rating, Bookmark, connect_to_db


def get_all_hikes():
    """Return all hikes"""

    return Hike.query.all()


def get_hikes_by_zip():
    """Given a zipcode, provide list of nearby hikes"""

    return Hike.query.all()


def create_hike(rating_id, location_id, city, latitude, longitude, zipcode, name, hike_length, average_rating, difficulty, route_type, activities, dog_friendly):
    """Create and return a new hike."""

    hike = Hike(rating_id = rating_id, location_id = location_id, city = city, latitude = latitude, longitude = longitude, zipcode = zipcode, name = name, hike_length = hike_length, average_rating=average_rating, difficulty = difficulty, route_type = route_type, activities = activities, dog_friendly = dog_friendly)

    db.session.add(hike)
    db.session.commit()

    return hike

def get_hike_details(hike_id):
    """Provide hike details including photo, length, etc."""

    return Hike.query.get(hike_id)


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


# For login 
def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()
    
    print(f"Successfully added student: {email}")

    return user

if __name__ == '__main__':
    from server import app
    connect_to_db(app)