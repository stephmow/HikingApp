"""Server for hike search app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_home():
    """Display homepage. Includes the following forms: 
    - form id = create-account
    - form id = user-login
    - form id = hike-search
    - List hikes (form hidden by image)
    - Hike details (form hidden by image) 
    """
    
    return render_template('homepage.html')


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
    # logged_in = False 

    if crud.get_user_by_email(user_email):
        if crud.get_user_by_email(user_email).password == user_password:
            session['user_email'] = user_email
            # logged_in = True 
            return "You are logged in."
        else:
            return "Incorrect password, try again"

    else:
        return "Email does not exist"


# @app.route('/hikeList')
# def hike_list():
#     """Displays list of hikes within search criteria"""

#     zipcode = int(request.args.get('zipcode'))

#     hikes = crud.get_all_hikes()
    
#     return render_template('all_hikes.html', hikes=hikes, zipcode=zipcode)

@app.route('/hikeList')
def hike_list():
    """Displays list of hikes within search criteria - update with ajax version for sprint 2 (later on)"""

    # zipcode = int(request.args.get('zipcode'))   
    zipcode = request.args.get('zipcode')   # for now, this will be a city search. 

    hikes = crud.get_all_hikes()
    
    return render_template('all_hikes.html', hikes=hikes, zipcode=zipcode)


@app.route('/hikeList/<hike_id>')
def hike_details(hike_id):
    """Show details on a particular hike"""

    hike = crud.get_hike_details(hike_id)

    return render_template("hike_details.html", hike=hike)


@app.route("/hikeList/<hike_id>/bookmark", methods=["POST"])
def create_bookmark(hike_id):
    """Create a bookmark for a hike."""

    logged_in_email = session.get("user_email")
    hike = crud.get_hike_details(hike_id)
    is_completed = request.form.get("bookmark")

    if is_completed == "True":
        is_completed = True
    elif is_completed == "False":
        is_completed = False
    else: 
        is_completed = None

#confirm i don't need the below code...since my hike_details already has an if statement to show the bookmarks module
    # if logged_in_email is None:
    #     # flash("You must log in to bookmark a hike.") 
    #     return redirect('/')
  
    if is_completed == False:  # Hike added to bookmarks
        user = crud.get_user_by_email(logged_in_email)
        hike = crud.get_hike_details(hike_id) 

        crud.create_bookmark(user=user, hike=hike, is_completed=is_completed)

        flash(f"You saved {{ hike.name }} to bookmarks.")

    elif is_completed == True: # Hike has been completed
        user = crud.get_user_by_email(logged_in_email)
        hike = crud.get_hike_details(hike_id) 
        
        crud.create_bookmark(user=user, hike=hike, is_completed=is_completed)

        flash(f"You completed {{ hike.name }}.")
        return('hikeList/<hike_id>/ratings')
    
    else:
        flash("Error: you didn't select a hike bookmark.")

    return redirect(f"/hikeList/{hike_id}")

@app.route("/hikeList/<hike_id>/add_bookmark", methods=["POST"])
def add_bookmark(hike_id):
    """AJAX route for adding a bookmark to save a hike."""

    is_completed = request.form.get("bookmark")
     
    if is_completed == "True":
        is_completed = True
    elif is_completed == "False":
        is_completed = False
    else: 
        is_completed = None

    logged_in_email = session.get("user_email")
    is_completed = request.form.get("bookmark")  # True or False 

    if is_completed == False:
        user = crud.get_user_by_email(logged_in_email)
        hike = crud.get_hike_by_id(hike_id)

        crud.create_bookmark(user, hike, is_completed)

        flash(f"You bookmarked this hike.")

    return redirect(f"/hikeList/{hike_id}")
    


@app.route("/hikeList/<hike_id>/add_ratings")
def create_rating(hike_id):
    """AJAX route for a rating for a hike."""
    
    is_completed = request.form.get("bookmark")
    rating = request.form.get("rating")
    comments = request.form.get("comments")
     
    if is_completed == "True":
        is_completed = True
    elif is_completed == "False":
        is_completed = False
    else: 
        is_completed = None

    logged_in_email = session.get("user_email")
    is_completed = request.form.get("bookmark")  # True or False 

    if is_completed == True:
        user = crud.get_user_by_email(logged_in_email)
        hike = crud.get_hike_by_id(hike_id)

        crud.create_rating(user, hike, rating, comments)

        flash(f"You created a rating for this hike.")

    return redirect(f"/hikeList/{hike_id}")
    


# @app.route("/hikeList/<hike_id>/ratings", methods=["POST"])
# def create_rating(hike_id):
#     """AJAX route for a rating for a hike."""

#     pass
       

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)