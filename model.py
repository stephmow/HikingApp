"""Models for hiking app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    # ratings = a list of Rating objects
    # bookmarks = a list of Bookmark objects

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


# class Hike(db.Model):
#     """A hike."""

#     __tablename__ = "hikes"

#     hike_id = db.Column(db.Integer,
#                         autoincrement=True,
#                         primary_key=True)
#     rating_id = db.Column(db.Integer)
#     location_id = db.Column(db.Integer)
#     name = db.Column(db.String(250))
#     zipcode = db.Column(db.Integer)  # add nullability
#     hike_length = db.Column(db.Integer)  # in miles
#     dog_friendly = db.Column(db.Boolean)  
#     average_rating = db.Column(db.Float)

#     # ratings = a list of Rating objects
#     # bookmarks = a list of Bookmark objects

#     def __repr__(self):
#         return f'<Hike hike_id={self.hike_id} name={self.name} zipcode={self.zipcode}>'


class Hike(db.Model):
    """A hike."""

    __tablename__ = "hikes"

    hike_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    rating_id = db.Column(db.Integer)
    location_id = db.Column(db.String)
    city = db.Column(db.String)
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)
    zipcode = db.Column(db.String)  # add nullability
    name = db.Column(db.String)
    hike_length = db.Column(db.Float)  # in miles
    average_rating = db.Column(db.Float)
    difficulty = db.Column(db.Integer)
    route_type = db.Column(db.String)
    activities = db.Column(db.String)
    dog_friendly = db.Column(db.Boolean)  

    # ratings = a list of Rating objects
    # bookmarks = a list of Bookmark objects

    def __repr__(self):
        return f'<Hike hike_id={self.hike_id} name={self.name} zipcode={self.zipcode}>'


class Rating(db.Model):
    """A hike rating."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    rating = db.Column(db.Integer)
    hike_id = db.Column(db.Integer, 
              db.ForeignKey("hikes.hike_id"))
    user_id = db.Column(db.Integer, 
              db.ForeignKey("users.user_id"))
    comments = db.Column(db.String(300))  # should this be in bookmarks instead??? 

    hike = db.relationship("Hike", backref="ratings")
    user = db.relationship("User", backref="ratings")

    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} rating={self.rating}>'


class Bookmark(db.Model):
    """A bookmarks of a hike that a user has completed or wants to do."""

    __tablename__ = "bookmarks"

    bookmark_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    hike_id = db.Column(db.Integer, 
                        db.ForeignKey("hikes.hike_id"))
    user_id = db.Column(db.Integer, 
                        db.ForeignKey("users.user_id"))
    is_completed = db.Column(db.Boolean)  
        # True = Completed; False = Wish List 

    hike = db.relationship("Hike", backref="bookmarks")
    user = db.relationship("User", backref="bookmarks")

    def __repr__(self):
        return f'<Bookmark hike_id={self.hike_id} is_completed={self.is_completed}'


def connect_to_db(flask_app, db_uri="postgresql:///hikedb", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
