"""Server for hiking app."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
import os

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
# RAPID_API_KEY = os.environ['RAPID_API_KEY'] 


@app.route('/')
def show_home():
    """Display homepage"""

    user_login = session.get("USER_EMAIL")
    user = crud.get_user_by_email(user_login)

    print("\n\n\ncurrent logged in user is from '/' route:", user_login)

    if user_login:
        bookmarks = crud.get_bookmarks_by_user_id(user.user_id)
        ratings = crud.get_ratings_by_user_id(user.user_id)
        return render_template('homepage.html', user_login=user_login, bookmarks=bookmarks, ratings=ratings)
    else: 
        return render_template('homepage.html', user_login=None)


@app.route('/loggedin')
def logged_in():
    """send bookmarks, ratings and google forms to homepage when logged in"""

    user_login = session.get("USER_EMAIL")
    user = crud.get_user_by_email(user_login)

    bookmarks = crud.get_bookmarks_by_user_id(user.user_id)
    print("\n\n\n\n****bookmarks[0]=",bookmarks[0])

    ratings = crud.get_ratings_by_user_id(user.user_id)
    print("\n\n\ncurrent logged in user is from '/loggedin' route: user_login is ", user_login)
    print("\n\n\ncurrent logged in user is from '/loggedin' route: session is ", session['USER_EMAIL'])


    return render_template('homepage_loggedin.html', user_login=user_login, ratings = ratings, bookmarks = bookmarks)


@app.route('/users', methods = ["POST"])
def create_account():
    """AJAX route for users to create account"""

    user_email = request.form.get('email')
    user_password = request.form.get('password')

    if crud.get_user_by_email(user_email):   # if user_email is in the User database
        flash("There is already an account with that email. Please log in.")
    else:
        crud.create_user(user_email, user_password)  # adds user to the User database
        flash("Your account is created. You can log in")

    return redirect('/')


@app.route('/login', methods = ["POST"])
def login():
    """AJAX route for users to login"""

    user_email = request.form.get('email')
    user_password = request.form.get('password')

    if crud.get_user_by_email(user_email):
        if crud.get_user_by_email(user_email).password == user_password:
            session['USER_EMAIL'] = user_email
            print("\n\nCURRENT SESSION from '/login' ****= ", session['USER_EMAIL'], "\n\n")
            return "You are logged in."
        else:
            return "Incorrect password, try again"

    else:
        return "Email does not exist"


@app.route('/bookmarks/map.json')
def bookmark_coordinates():
    """Return coordinates for all users bookmarked hikes"""

    user_login = session.get("USER_EMAIL")
    user = crud.get_user_by_email(user_login)

    print("\n\n\n user session*** = ", user_login)

    print("\n user = ", user.user_id, "\n\n")    

    bookmark_list = crud.get_bookmark_coords(user.user_id)

    print("\n\nbookmark list = ", bookmark_list, "\n\n")

    return jsonify((bookmark_list))


@app.route('/ratings/map.json')
def rating_coordinates():
    """Return coordinates for all users rated/completed hikes"""

    user_login = session.get("USER_EMAIL")
    user = crud.get_user_by_email(user_login)

    # print("\n user = ", user.user_id, "\n\n")    

    ratings_list = crud.get_rating_coords(user.user_id)

    return jsonify((ratings_list))



@app.route('/hikeList')
def hike_list():
    """Displays list of hikes within search criteria"""

    input = request.args.get('location-input')   # SEARCH BY ZIPCODE, CITY OR NAME 
    hikes = crud.get_all_hikes()

    return render_template('all_hikes.html', hikes=hikes, input=input)


@app.route('/logout')
def user_logout():
    """Logout user"""

    session.clear()
    return redirect('/')


@app.route('/hikeList/<hike_id>')
def hike_details(hike_id):
    """Show details on a particular hike"""

    hike = crud.get_hike_details(hike_id)
    session['CURRENT_HIKE'] = hike_id
    user_login = session.get("USER_EMAIL")

    print("\n\nuser_login**", user_login, "\n\n")
    print("\n\nCURRENT_HIKE", session['CURRENT_HIKE'], "\n\n")
    
    return render_template("hike_details.html", hike=hike, user_login=user_login)


@app.route('/hikeList/<hike_id>/map.json')
def hike_coordinates(hike_id):
    """Return coordinates for a particular hike"""

    hike_coord = crud.get_hike_coords(hike_id)

    # print("\n\nHIKE COORDINATES = ", hike_coord, "\n\n")

    return (hike_coord)


@app.route("/hikeList/<hike_id>/add_bookmark", methods=["POST"])
def add_bookmark(hike_id):
    """AJAX route for adding a bookmark to save a hike."""

    # is_completed = request.form.get("bookmark") # use this if accessing through form
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
            # print("\n ", bookmark['hike_id'])
            # print("\n\n current hike session is", session["CURRENT_HIKE"])
            if int(bookmark['hike_id']) == int(session['CURRENT_HIKE']):
                # print('\n\n\n******HIKE IS ALREADY BOOKMARKED******')
                return("Hike has already been saved. See homepage for bookmarks.")
        
        user = crud.get_user_by_email(session['USER_EMAIL'])
        hike = crud.get_hike_details(session['CURRENT_HIKE'])

        crud.create_bookmark(user = user, hike = hike, is_completed = is_completed)
        # print('\n\n\n******HIKE BOOKMARKED******')

        return ('This hike has been saved!')
    

@app.route("/hikeList/<hike_id>/add_rating", methods=["POST"])
def create_rating(hike_id):
    """AJAX route for a rating for a hike."""

    is_completed = request.form.get("is_completed")
    user_rating = request.form.get("rating")
    comments = request.form.get("comments")
    user_login = session.get("USER_EMAIL")

    # print("\n\n\n rating is = ", user_rating)
     
    if is_completed == "True":
        is_completed = True
    elif is_completed == "False":
        is_completed = False
    else: 
        is_completed = None     

    ratings = crud.get_ratings_by_user_email(user_login)

    print(ratings)

    if is_completed == True:
        for rating in ratings:
            # print("\n ", rating['hike_id'])
            # print("\n\n current hike session is", session["CURRENT_HIKE"])
            if int(rating['hike_id']) == int(session['CURRENT_HIKE']):
                # print('\n\n\n******HIKE has already been rated******')
                return('You already completed and rated this hike.')
        
        user = crud.get_user_by_email(session['USER_EMAIL'])
        hike = crud.get_hike_details(session['CURRENT_HIKE'])

        crud.create_rating(user = user, hike = hike, rating = user_rating, comments = comments)

        crud.delete_bookmark(user = user, hike = hike)

        # print('\n\n\n******HIKE rated******')
        return('Rating added for this hike.')


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)