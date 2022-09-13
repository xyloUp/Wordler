from flask import Blueprint, request, redirect, url_for, render_template, session
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    
    from .scripts import EditTxt

    session["word"] = EditTxt.get_random_word()
    print("Created New Word", session["word"])

    return render_template("home.html", user=current_user)

@views.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)