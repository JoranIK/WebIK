import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# let CS50 use SQL for our database
db = SQL("sqlite:///WebIK22.db")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # checks if username is not empty
        if not request.form.get("username"):
            return apology("Username can not be empty", 400)

        # checks if username is available
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        if len(rows) >= 1:
            return apology("Username already exists", 400)

        # checks if password and confirmation are not empty
        if not request.form.get("password") or not request.form.get("confirmation"):
            return apology("Password can not be empty", 400)

        # checks if password and confirmation match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Your password doesn't match", 400)

        # inserts data into database, and hashes password
        db.execute("INSERT INTO users (username, hash) VALUES(:username, :password)",
                   username=request.form.get("username"), password=generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8))

        # return to homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("register.html")


@app.route("/instruments", methods=["GET", "POST"])
def instruments():
    return render_template("instruments.html")