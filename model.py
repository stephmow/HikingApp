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

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'
        

class Hike(db.Model):
    """A hike."""

    __tablename__ = "hikes"

    hike_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    rating_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
    zipcode = db.Column(db.Integer)
    hike_length = db.Column(db.Integer)  # in miles
    dog_friendly = db.Column(db.Boolean)  # is this right? 
    average_rating = db.Column(db.Integer)

    # ratings = a list of Rating objects

    def __repr__(self):
        return f'<Hike hike_id={self.hike_id} zipcode={self.zipcode}>'


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

    # movie = db.relationship("Movie", backref="ratings")
    # user = db.relationship("User", backref="ratings")


    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} score={self.score}>'


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
    is_completed = db.Column(db.Boolean)  # True = Completed; False = Wish List 
    
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
