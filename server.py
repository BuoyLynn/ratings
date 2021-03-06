"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("users-list.html", users=users)


@app.route('/register', methods=['GET', 'POST'])
def registration():
    # add query that checks if email in db, if not
    # create account
   
    email = request.args.get("email")
    password = request.args.get("password")
    age = request.args.get("age")
    zipcode = request.args.get("zipcode")

    list_email = db.query.filter_by(email).all()

    if email in list_email:
    
        flash("User already exists.")
        return redirect("/")
    
    else:

        db.session.add(email, password, age, zipcode)
        db.session.commit()

        flash("Logged in")
        return render_template("register-form.html", email=email,
                                                     password=password,
                                                     age=age,
                                                     zipcode=zipcode)

@app.route('/movies')
def all_movies():

    return render_template("movies.html")
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
