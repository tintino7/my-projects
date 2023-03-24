import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, lookup, lookup_id
from datetime import datetime

# Configure application
app = Flask(__name__)

# Custom filter


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///meals.db")






@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Recipes in bookmark
    bookmark = db.execute("SELECT * FROM bookmark WHERE id = ?", session["user_id"])

    # User reached via route post (by searching the meal by ingredient)
    if request.method == "POST":
        # call lookup for meal information
        ingredient = request.form.get("ingredient")
        mealinfo = lookup(ingredient)
        

        # if user entered a invalid ingredient
        if (mealinfo == None):
            apology = "Enter a valid ingredient"
            return render_template("quote.html",apology=apology)
        # user entered valid ingredient
        else:
            apology = 0
            return render_template("quote.html", mealinfo=mealinfo, apology=apology)



    # user reached via route get
    else:
        # get meal id from bookmark table
        bookmarked = db.execute("SELECT mealid FROM bookmark WHERE id = ?",session["user_id"])
        
        meals = []
        # for every id in bookmarked call lookup id
        for id in bookmarked:
            mealinfo = lookup_id(id['mealid'])
            meals.append(mealinfo)

        return render_template("index.html", meals=meals)    


# route for sending dynamic content to modal
@app.route('/get_dynamic_content', methods=['POST'])
def get_dynamic_content():
    # Get the data posted in the request
    data = request.get_json()   

    # call lookup id function to get meal info for the id
    recipeinfo = lookup_id(data['name'])

    


    if (recipeinfo == None):
        # Code to generate dynamic content based on the data
        dynamic_content = {'title': data['name'], 'body': data['name']}

        # Return the dynamic content as JSON
        return jsonify(dynamic_content)    
    else:
        # Code to generate dynamic content based on the data
        dynamic_content = {'title': recipeinfo['name'], 'body': recipeinfo['instr'], 'img': recipeinfo['img'], 'yt': recipeinfo['yt']}

        # Return the dynamic content as JSON
        return jsonify(dynamic_content)


@app.route('/bookmark_meal', methods=["POST"])
def bookmark_meal():

    # Get the id posted
    data = request.get_json()

    # Get all the info by calling lookup
    recipeinfo = lookup_id(data['id'])

    # insert the data into database bookmark table
    db.execute("INSERT INTO bookmark (id, mealid, recipelink, mealname) VALUES(?,?,?,?)",session["user_id"], recipeinfo["id"], recipeinfo["yt"],recipeinfo["name"])   

    result = {"status":"Sucess"}
    return jsonify(result)



@app.route("/bookmark", methods=["GET", "POST"])
@login_required
def bookmark():
    
    # if user reaches via post
    if request.method == "POST":

        # get mealid
        id = request.form.get("mealid")
        db.execute("DELETE FROM bookmark WHERE mealid = ?",id)

        bookmarked = db.execute("SELECT * FROM bookmark WHERE id = ?",session["user_id"])

        return render_template("bookmark.html", bookmarked=bookmarked)
    else:
        # Get meal information from data base
        bookmarked = db.execute("SELECT * FROM bookmark WHERE id = ?",session["user_id"])
        return render_template("bookmark.html", bookmarked=bookmarked)
        
    

@app.route("/userinfo")
@login_required
def userinfo():
    """Show history of transactions"""
    info = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    return render_template("userinfo.html", info=info)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":


        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1:
            # sent error message
            message = "Invalid username or password !!!"
            return render_template("login.html", message=message)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")




@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")






@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # if users reached via post
    if request.method == "POST":
        # get inputs from user
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirm")
        # check for username availability
        if username:
            usersname = db.execute("SELECT id FROM users WHERE username = ?", username)

            # if username already exists
            if usersname:

                # error message for user name already exists
                message = "User name already exists"
                return render_template("register.html", message=message)
        

        # ensure password matches with confirmation
        if password != confirmation:

            # sent error for password not matching confirmation
            message = "Password must match confirmation"
            return render_template("register.html", message=message)

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
        # redirect user to login
        return redirect("/login")


    # users reached via GET
    else:
        return render_template("register.html")



    


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """ Change password """
    # user access via post
    if request.method == "POST":
        old_password = request.form.get("password")
        new_password = request.form.get("newpassword")
        confirm_password = request.form.get("confirm")

        hash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        # check for correct old password
        if check_password_hash(hash[0]["hash"], old_password) == False:
            apology = "Enter a valid password"
            return render_template("changepassword.html", apology=apology)


        # make sure new password and confirm password are same
        if new_password != confirm_password:
            apology = "confirm must match new password"
            return render_template("changepassword.html", apology=apology)

        # entry new changed password into users
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new_password), session["user_id"])
        
        return redirect("/")
    else:
        return render_template("changepassword.html")