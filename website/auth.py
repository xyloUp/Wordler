from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, login_user, logout_user, current_user
from httpx import post

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        req = post(f"{request.host_url}/auth/login", json=dict(request.form))
        if req.status_code in range(200, 205):
            from .api.api import Auth
            account = Auth().account_exists(**request.form)
            if account:
                login_user(account)
                flash("Loggin In Successfully", category="successs")
                return redirect(url_for("views.home"))
            else:
                flash("Unable To Login", category="error")
                return redirect(url_for(".login"))   
        elif req.status_code in range(400, 405):    
            flash("Invalid Credentials", category="error")

    return render_template("login.html", user=current_user)

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        req = post(f"{request.host_url}/auth/register", json=dict(request.form))
        if req.status_code in range(200, 205):
            from .api.api import Auth
            account = Auth().account_exists(**request.form)
            if account:
                login_user(account)
                flash("Account Registered Successsfully", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Account Registered Successsfully But Unable To Login.", category="success")
                return redirect(url_for(".login"))   
        elif req.status_code == 400:
            flash("Account Already Exists!", category="error")
             
    return render_template("register.html", user=current_user)

@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("Loggout Out Successfully!", category="success")
    return redirect(url_for(".login"))

@auth.route("/delete-account", methods=["GET", "POST"])
@login_required
def delete_account():

    from .api.api import Auth

    if hasattr(current_user, "username"):
        Auth().delete_account(current_user.username)
        flash("Deleted Account Successfully!", category="success")
        return redirect(url_for(".login"))
    flash("Failed To Delete Account!", category="error")
    return redirect(url_for("views.home"))

    