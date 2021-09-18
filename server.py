"""Server for hiking app."""

from flask import (Flask, render_template, request, session, redirect, jsonify)
from model import Bookmark, Hike, User, Rating, connect_to_db
import crud
from jinja2 import StrictUndefined
import os

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
# RAPID_API_KEY = os.environ['RAPID_API_KEY'] Not currently using RapidAPI hiking data. 


@app.route('/')
def show_home():
    """Display homepage"""

    user_login = session.get("USER_EMAIL")
    user = crud.get_user_by_email(user_login)

    if user_login:

        bookmarks = crud.get_bookmarks_by_user_id(user.user_id)
        ratings = crud.get_ratings_by_user_id(user.user_id)

        return render_template('homepage.html', user_login=user_login, bookmarks=bookmarks, ratings=ratings)

    else: 
        return render_template('homepage.html', user_login=None)


@app.route('/search.json')
def search():
    """Return list of all hikes within search criteria"""
    
    hikes = crud.get_hike_search()  

    return jsonify(hikes) 


@app.route('/loggedin')
def logged_in():
    """Send bookmarks, ratings and google map divs to homepage when logged in"""

    user_login = session.get("USER_EMAIL")
    user = crud.get_user_by_email(user_login)

    bookmarks = crud.get_bookmarks_by_user_id(user.user_id)
    ratings = crud.get_ratings_by_user_id(user.user_id)

    return render_template('homepage-loggedin.html', user_login = user_login, ratings = ratings, bookmarks = bookmarks)


@app.route('/users', methods = ["POST"])
def create_account():
    """AJAX route for users to create account"""

    user_email = request.form.get('email')
    user_password = request.form.get('password')

    if crud.get_user_by_email(user_email):   
        return "There is already an account with that email. Please log in."

    else:
        crud.create_user(user_email, user_password)  
        return "Your account is created. You can log in"


@app.route('/login', methods = ["POST"])
def login():
    """AJAX route for users to login"""

    user_email = request.form.get('email')
    print(user_email)
    user_password = request.form.get('password')

    if crud.get_user_by_email(user_email) is None: 
        return "Email not registered. Please create account."
    elif crud.get_user_by_email(user_email).password == user_password:
        session['USER_EMAIL'] = user_email
        return "You are logged in."
    else:
        return "Incorrect email or password. Please try again."


@app.route('/logout')
def user_logout():
    """Logout user"""

    session.clear()

    return redirect('/')


@app.route('/bookmarks/map.json')
def bookmark_coordinates():
    """Return coordinates for all users bookmarked hikes"""

    user_login = session.get("USER_EMAIL")
    user = crud.get_user_by_email(user_login)  
    bookmark_list = crud.get_bookmark_coords(user.user_id)

    return jsonify((bookmark_list))


@app.route('/ratings/map.json')
def rating_coordinates():
    """Return coordinates for all users rated/completed hikes"""

    user_login = session.get("USER_EMAIL")
    user = crud.get_user_by_email(user_login)
    ratings_list = crud.get_rating_coords(user.user_id)

    return jsonify((ratings_list))


@app.route('/hikeList')
def hike_list():
    """Displays list of hikes within search criteria. Users can search by zipcode, city or name"""

    input = request.args.get('location-input') 
    hikes = crud.get_all_hikes()
    user_login = session.get("USER_EMAIL")

    return render_template('all_hikes.html', hikes=hikes, input=input, user_login = user_login)


@app.route('/delete_bookmark', methods = ["POST"])
def delete_bookmark():
    """Deletes corresponding bookmark"""

    hike_id = request.form.get('hike-id')  # receives hike-id from 'home.js' post 
    user_login = session.get("USER_EMAIL")
    user = crud.get_user_by_email(user_login)

    crud.delete_bookmark(user = user, hike_id = hike_id) 

    return "Bookmark has been deleted."


@app.route('/delete_rating', methods = ["POST"])
def delete_rating():
    """Deletes corresponding rating"""

    hike_id = request.form.get('hike-id')  # receives hike-id from 'home.js' post 
    user_login = session.get("USER_EMAIL")
    user = crud.get_user_by_email(user_login)

    crud.delete_rating(user = user, hike_id = hike_id) 

    return "Rating for {{hike_id}} has been deleted."


@app.route('/hikeList/<hike_id>')
def hike_details(hike_id):
    """Show details on a particular hike"""

    hike = crud.get_hike_details(hike_id)
    session['CURRENT_HIKE'] = hike_id
    user_login = session.get("USER_EMAIL")
    ratings = crud.get_ratings_by_user_email(user_login)
    bookmarks = crud.get_bookmarks_by_user_email(user_login)
    
    return render_template("hike_details.html", hike=hike, user_login=user_login, ratings = ratings, bookmarks = bookmarks)


@app.route('/hikeList/<hike_id>/map.json')
def hike_coordinates(hike_id):
    """Return coordinates for a particular hike"""

    hike_coord = crud.get_hike_coords(hike_id)

    return (hike_coord)


@app.route("/hikeList/<hike_id>/add_bookmark", methods=["POST"])
def add_bookmark(hike_id):
    """AJAX route for adding a bookmark to save a hike."""

    is_completed = request.form.get("is_completed") # taking in input from ratings.js
    user_login = session.get("USER_EMAIL")

    if is_completed == "True":
        is_completed = True
    elif is_completed == "False":
        is_completed = False
    else: 
        is_completed = None
    
    bookmarks = crud.get_bookmarks_by_user_email(user_login)
    
    if is_completed == False:
        for bookmark in bookmarks:
            if int(bookmark['hike_id']) == int(session['CURRENT_HIKE']):
                return("Hike has already been saved. See homepage for bookmarks.")
        
        user = crud.get_user_by_email(session['USER_EMAIL'])
        hike = crud.get_hike_details(session['CURRENT_HIKE'])

        crud.create_bookmark(user = user, hike = hike, is_completed = is_completed)

        return ('This hike has been saved!')
    

@app.route("/hikeList/<hike_id>/add_rating", methods=["POST"])
def create_rating(hike_id):
    """AJAX route for a rating for a hike."""

    is_completed = request.form.get("is_completed")
    user_rating = request.form.get("rating")
    comments = request.form.get("comments")
    user_login = session.get("USER_EMAIL")
     
    if is_completed == "True":
        is_completed = True
    elif is_completed == "False":
        is_completed = False
    else: 
        is_completed = None     

    ratings = crud.get_ratings_by_user_email(user_login)
    bookmarks = crud.get_bookmarks_by_user_email(user_login)

    print(ratings)

    user = crud.get_user_by_email(session['USER_EMAIL'])
    hike = crud.get_hike_details(session['CURRENT_HIKE'])

    if is_completed == True:
        for rating in ratings:
            if int(rating['hike_id']) == int(session['CURRENT_HIKE']):
                return('You already completed and rated this hike.')

        crud.create_rating(user = user, hike = hike, rating = user_rating, comments = comments)

        for bookmark in bookmarks:
            if int(bookmark['hike_id']) == int(session['CURRENT_HIKE']):
                crud.delete_bookmark(user = user, hike_id = hike_id)

        return('Rating added for this hike.')
        

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)