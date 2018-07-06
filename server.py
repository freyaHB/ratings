"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined()


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""
    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/register', methods=["GET"])
def register_form():
    return render_template("register_form.html")

@app.route('/register', methods=["POST"])
def register_process():
    user_email = request.form.get("email")
    password = request.form.get("password")

    query = User.query.filter(User.email == user_email).first()
    
    if query is None:
        new_user = User(email=user_email, password=password)
        db.session.add(new_user)
        db.session.commit()
    return redirect("/")

@app.route('/user-login', methods=["GET"])
def login_form():
    return render_template("login_form.html")

@app.route("/user-login", methods=["POST"])
def handle_login():
    """logs an existing user in after they register"""
    user_email = request.form.get('email')
    password = request.form.get('password')
     #user_id = User.query.filter(User.email)

    #query = User.query.filter(User.email==user_email, User.password == password).first()
    user = User.query.filter(User.email == user_email).first()

    if user is not None:
        if user.password == password:
            session["user_name"] = user.user_id
            flash("Logged in")
            return redirect("/")
        else: 
            flash("Password is incorrect!")
            return redirect("/user-login")
    else: 
        flash("Incorrect email, please register")
        return redirect ("/register")        

    # if query:
    #     session['email'] = user_email
    #     session['user_id'] = query.user_id
    #     flash("Logged in as %s" % user_email)
    #     return redirect("/")
    # else:
    #     flash("Wrong password!")
    #     return redirect("/user-login")        

@app.route('/users/<user_id>')
def show_user_profile(user_id):
    user = User.query.filter(User.user_id == user_id).first()
    #age = user.age
    #zipcode = user.zipcode

    #return "Profile page for user: {}".format(user_id)
    return render_template("user_info.html", user=user)

@app.route('/movies')
def show_movie_list():
    movies = Movie.query.order_by(Movie.title).all()

    return render_template("movie_list.html", movies=movies)

@app.route('/movie/<movie_id>')
def display_movie_page(movie_id):
    movie_info = Movie.query.filter(Movie.movie_id == movie_id).first()

    return render_template("movie_info.html", movie_info=movie_info)
                




    


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
