import requests
import urllib.parse
import os

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def skill_counter(wants, user_info):
    skill_levels = dict()
    for item in wants:
        if item == "want_guitar":
            if user_info["likes_guitar"] <= 10:
                skill_levels["guitar"] = "beginner"
            if user_info["likes_guitar"] > 10:
                skill_levels["guitar"] = "competent"
            if user_info["likes_guitar"] > 20:
                skill_levels["guitar"] = "proficient"
            if user_info["likes_guitar"] > 30:
                skill_levels["guitar"] = "expert"

        if item == "want_electric_guitar":
            if user_info["likes_electric_guitar"] <= 10:
                skill_levels["electric_guitar"] = "beginner"
            if user_info["likes_electric_guitar"] > 10:
                skill_levels["electric_guitar"] = "competent"
            if user_info["likes_electric_guitar"] > 20:
                skill_levels["electric_guitar"] = "proficient"
            if user_info["likes_electric_guitar"] > 30:
                skill_levels["electric_guitar"] = "expert"

        if item == "want_piano":
            if user_info["likes_piano"] <= 10:
                skill_levels["piano"] = "beginner"
            if user_info["likes_piano"] > 10:
                skill_levels["piano"] = "competent"
            if user_info["likes_piano"] > 20:
                skill_levels["piano"] = "proficient"
            if user_info["likes_piano"] > 30:
                skill_levels["piano"] = "expert"

        if item == "want_drums":
            if user_info["likes_drum"] <= 10:
                skill_levels["drum"] = "beginner"
            if user_info["likes_drum"] > 10:
                skill_levels["drum"] = "competent"
            if user_info["likes_drum"] > 20:
                skill_levels["drum"] = "proficient"
            if user_info["likes_drum"] > 30:
                skill_levels["drum"] = "expert"

    return skill_levels
