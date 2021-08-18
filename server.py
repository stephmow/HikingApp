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
    """Display homepage. Includes search for hike form"""
    
    return render_template('homepage.html')

@app.route('/hikeList')
def hike_list():
    """Displays list of hikes within search criteria"""

    hikes = crud.get_hikes_by_zip()
    
    return render_template('all_hikes.html', hikes=hikes)


@app.route('/hikeList/<int:hike_id>')
def hike_details(hike_id):
    
    hike = crud.get_hike_by_id(hike_id)

    return render_template("hike_details..html", hike=hike)


@app.route("/users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)

       
@app.route('/users', methods = ["POST"])
def create_account():

    user_email = request.form.get('email')
    user_password = request.form.get('password')

    if crud.get_user_by_email(user_email):
        flash("There is already an account with that email.")
    else:
        crud.create_user(user_email, user_password)
        flash("Your account is created. You can log in")

    return redirect('/')


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)


@app.route('/login', methods = ["POST"])
def login():

    user_email = request.form.get('email')
    user_password = request.form.get('password')

    if crud.get_user_by_email(user_email):
        if crud.get_user_by_email(user_email).password == user_password:
            session['user_email'] = user_email
            flash("Logged in!")
            return render_template('logged_in.html')
        else:
            flash("Incorrect password, try again.")

    else:
        flash("Email does not exist.")

    return redirect('/')



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)