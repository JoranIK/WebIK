import os
import sys
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required, skill_counter, like_instrument, dislike_instrument

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


@app.route("/upload", methods=["GET", "POST"])
def upload():
    # if button is clicked
    if request.method == "POST":
        # set variables for filled in fields
        user_id = session["user_id"]
        video_id = request.form.get("video_id")
        video_name = request.form.get("video_name")
        instrument = request.form.get("instruments-select")
        skill_level = request.form.get("level-select")

        # insert video in db
        db.execute("INSERT INTO video (id, video_id, video_name, instrument, skill_level) VALUES (:user_id, :video_id, :video_name, :instrument, :skill_level)",
                   user_id=user_id, video_id=video_id, video_name=video_name, instrument=instrument, skill_level=skill_level)

        return render_template("upload1.html")
    return render_template("upload.html")


@app.route("/like", methods=["GET"])
@login_required
def like():

    # set variables
    video_id = request.args.get("video_id")
    liker_id = session["user_id"]
    video_info = db.execute("SELECT * FROM video WHERE video_id=:video_id",
                            video_id=video_id)
    poster_id = video_info[0]["id"]
    instrument = video_info[0]["instrument"]

    # likes poster's instrument counter
    like_instrument(instrument, poster_id, db)

    # insert like into db
    db.execute("INSERT INTO likes (poster_id, video_id, liker_id) VALUES (:poster_id, :video_id, :liker_id)",
               poster_id=poster_id, video_id=video_id, liker_id=liker_id)

    return '', 204


@app.route("/dislike", methods=["GET"])
@login_required
def dislike():

    # set variables
    video_id = request.args.get("video_id")
    liker_id = session["user_id"]
    video_info = db.execute("SELECT * FROM video WHERE video_id=:video_id",
                            video_id=video_id)
    poster_id = video_info[0]["id"]
    instrument = video_info[0]["instrument"]

    # dislikes poster's instrument counter
    dislike_instrument(instrument, poster_id, db)

    # delete like from db
    db.execute("DELETE FROM likes WHERE poster_id = :poster_id AND video_id = :video_id AND liker_id = :liker_id",
               poster_id=poster_id, video_id=video_id, liker_id=liker_id)

    return '', 204


@app.route("/follow", methods=["GET"])
@login_required
def follow():

    # sets master and slave id, slave follows the master
    master_id = request.args.get("user_id")
    slave_id = session['user_id']

    # make a list of user the user is already following
    db_followers = db.execute("SELECT master_id FROM followers WHERE slave_id = :slave_id",
                              slave_id=slave_id)
    already_following = [item['master_id'] for item in db_followers]

    # if the connection already exists, don't allow the follow
    exists = db.execute("SELECT master_id, slave_id FROM followers WHERE master_id = :master_id AND slave_id = :slave_id",
                        master_id=master_id, slave_id=slave_id)
    if not exists:
        db.execute("INSERT INTO followers (master_id, slave_id) VALUES(:master_id, :slave_id)",
                   master_id=master_id, slave_id=slave_id)

    return '', 204


@app.route("/unfollow", methods=["GET"])
@login_required
def unfollow():

    master_id = request.args.get("user_id")
    slave_id = session['user_id']

    # make a list of users the user is already following
    db_followers = db.execute("SELECT master_id FROM followers WHERE slave_id = :slave_id",
                              slave_id=slave_id)
    already_following = [item['master_id'] for item in db_followers]

    # if the connection already exists, only then unfollow
    exists = db.execute("SELECT master_id, slave_id FROM followers WHERE master_id = :master_id AND slave_id = :slave_id",
                        master_id=master_id, slave_id=slave_id)
    if exists:
        db.execute("DELETE FROM followers WHERE master_id = :master_id AND slave_id = :slave_id",
                   master_id=master_id, slave_id=slave_id)

    return '', 204


@app.route("/search", methods=["GET", "POST"])
def search():

    if session['user_id']:
        # make a list of users without the currently logged in user
        user_id = session['user_id']
        userlist = db.execute("SELECT username, id FROM users WHERE NOT id=:user_id",
                              user_id=user_id)
    else:
        # make a list of all users
        userlist = db.execute("SELECT username, id FROM users")

    if session['user_id']:
        db_followers = db.execute("SELECT master_id FROM followers WHERE slave_id = :slave_id",
                                  slave_id=session['user_id'])
        already_following = [item['master_id'] for item in db_followers]

    # make a dict that matches username and id together
    results = dict()
    if request.method == "POST":
        for item in userlist:
            if request.form.get("searchfield") in item['username']:
                results[item['username']] = item['id']
    return render_template("search.html", results=results, already_following=already_following)


@app.route("/logout")
def logout():

    session.clear()

    return render_template("logout.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():

    user_info = db.execute("SELECT * FROM users WHERE id = :id",
                           id=session['user_id'])[0]

    user_videos = db.execute("SELECT * FROM video WHERE id = :id",
                             id=session["user_id"])

    # if the user is logged in, make a list of who he's following
    if session['user_id']:
        master_list = db.execute("SELECT master_id FROM followers WHERE slave_id = :slave_id",
                                 slave_id=session['user_id'])
        following = [item['master_id'] for item in master_list]
        usernames_ids = db.execute("SELECT username, id FROM users")
        following_usernames = dict()

        for pair in usernames_ids:
            for following_id in following:
                if following_id == pair['id']:
                    following_usernames[pair['username']] = following_id

    # make a list with the instruments the user wants to play
    wants = [item for item in user_info if user_info[item] == 'yes' and item.startswith('want')]

    # set skill level based on likes on instrument user wants to learn
    skill_levels = skill_counter(wants, user_info)

    return render_template("profile.html", user_info=user_info, wants=wants, following_usernames=following_usernames, user_videos=user_videos, skill_levels=skill_levels)


@app.route("/userprofile", methods=["GET"])
def userprofile():

    id = request.args.get("id")

    user_info = db.execute("SELECT * FROM users WHERE id = :id",
                           id=id)[0]

    user_videos = db.execute("SELECT * FROM video WHERE id = :id",
                             id=id)

    wants = [item for item in user_info if user_info[item] == 'yes' and item.startswith('want')]

    # set skill level based on likes on instrument user wants to learn
    skill_levels = skill_counter(wants, user_info)

    return render_template("userprofile.html", user_info=user_info, wants=wants, user_videos=user_videos, skill_levels=skill_levels)


@app.route("/profileeditor", methods=["GET", "POST"])
def profileeditor():

    user_info = db.execute("SELECT * FROM users WHERE id = :id",
                           id=session['user_id'])[0]

    # if the field is empty, keep the already existing information
    if request.method == "POST":
        name = request.form.get("name")
        if name == "":
            name = user_info['name']
        city = request.form.get("city")
        if city == "":
            city = user_info['city']
        birthday = request.form.get("birthday")
        if birthday == "":
            birthday = user_info['birthday']
        picture_url = request.form.get("picture_url")
        if picture_url == "":
            picture_url = user_info['picture_url']
        description = request.form.get("description")
        if description == "":
            description = user_info['description']

        db.execute("UPDATE users set name = :name, city = :city, birthday = :birthday, picture_url = :picture_url, description = :description WHERE id = :id",
                   name=name, city=city, birthday=birthday, picture_url=picture_url, description=description, id=session['user_id'])

        return redirect("/profile")

    return render_template("/profileeditor.html", user_info=user_info)


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

        if not request.form.get("email"):
            return apology("Email can not be empty", 400)

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

        # set yes if user wants to learn instrument
        if request.form.get("want-guitar") == "on":
            want_guitar = "yes"
        else:
            want_guitar = "no"

        if request.form.get("want-electric-guitar") == "on":
            want_electric_guitar = "yes"
        else:
            want_electric_guitar = "no"

        if request.form.get("want-piano") == "on":
            want_piano = "yes"
        else:
            want_piano = "no"

        if request.form.get("want-drums") == "on":
            want_drums = "yes"
        else:
            want_drums = "no"

        # inserts data into database, and hashes password
        db.execute("INSERT INTO users (username, password, want_guitar, want_electric_guitar, want_piano, want_drums, email) VALUES(:username, :password, :want_guitar, :want_electric_guitar, :want_piano, :want_drums, :email)",
                   username=request.form.get("username"), password=generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8), want_guitar=want_guitar, want_electric_guitar=want_electric_guitar, want_piano=want_piano, want_drums=want_drums, email=request.form.get("email"))

        # return to homepage, registration is successful
        return render_template("register1.html")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to login home page
        return render_template("homepage.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/instruments", methods=["GET", "POST"])
def instruments():
    instrument = request.args.get("instruments-select")
    skill_level = request.args.get("level-select")

    videos = db.execute("SELECT * FROM video WHERE instrument = :instrument AND skill_level = :skill_level",
                        instrument=instrument, skill_level=skill_level)

    if not videos:
        return render_template("instruments.html")

    return render_template("instruments.html", videos=videos)


@app.route("/registercheck", methods=["GET"])
def registercheck():

    # make a list of existing usernames
    usernames = db.execute("SELECT username FROM users")
    taken_names = [item['username'] for item in usernames]

    # check if the entered username is available
    username = request.args.get('username')
    if username in taken_names:
        available = 'false'
    else:
        available = 'true'

    return available


@app.route("/usercheck", methods=["GET"])
def usercheck():

    # make a list of existing usernames
    usernames = db.execute("SELECT username FROM users")
    taken_names = [item['username'] for item in usernames]

    # request the users input
    username = request.args.get('username')
    password = request.args.get('password')

    # check if the password of given username is correct with the given password
    db_password = db.execute("SELECT password FROM users WHERE username = :username",
                             username=username)
    if len(db_password) == 1:
        pw_check = check_password_hash(db_password[0]["password"], password)

    # define error codes
    error_code = '13'
    if len(username) == 0 and len(password) == 0:
        error_code = '13'
    elif len(username) == 0:
        error_code = '19'
    elif len(password) == 0:
        error_code = '93'
    elif username not in taken_names:
        error_code = '29'
    elif not pw_check:
        error_code = '94'
    else:
        error_code = '99'

    return error_code


@app.route("/video", methods=["GET", "POST"])
def video():
    videoId = request.args.get('video_id')

    # if a user is logged in, check if he already liked the video or not
    try:
        if session['user_id']:
            db_likes = db.execute("SELECT liker_id FROM likes WHERE video_id = :video_id",
                                  video_id=videoId)
            already_liked = [item['liker_id'] for item in db_likes]
            if session['user_id'] in already_liked:
                liked = True
            else:
                liked = False
    except KeyError:
        liked = False

    # see how many times the video was liked
    liked_by = db.execute("SELECT * FROM likes WHERE video_id = :video_id",
                          video_id=videoId)
    likes = 0
    for item in liked_by:
        likes += 1

    # only allow POST when user is logged in

    if request.method == "POST":
        if session['user_id']:
            db.execute("INSERT INTO comments (user_id, video_id, date, message) VALUES(:user_id, :video_id, :date, :message)",
                       user_id=session["user_id"], video_id=videoId, date=datetime.datetime.now(), message=request.form.get("comment"));

    currentVideo = db.execute("SELECT video_name, video_id FROM video WHERE video_id = :video_id", video_id=videoId)[0];
    comments = db.execute("SELECT * FROM comments JOIN users on comments.user_id = users.id WHERE comments.video_id = :video_id",
                          video_id=videoId);

    return render_template("video.html", video=currentVideo, comments=comments, liked=liked, likes=likes)


@app.route("/delete-comment/<commentId>", methods=["POST"])
def deleteComment(commentId):

    if session['user_id']:
        comment = db.execute("SELECT * FROM comments WHERE comment_id = :comment_id", comment_id=commentId)[0];
        user_id = comment["user_id"];

        # only allow user that has logged in to delete his or her comments
        if user_id == session['user_id']:
            db.execute("DELETE FROM comments WHERE comment_id = :comment_id", comment_id=commentId);
            return 'Ok', 200;

    return 'Unauthorized', 401;
