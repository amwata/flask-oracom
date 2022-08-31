from flask import render_template, Blueprint, url_for, flash, redirect
from flask_login import logout_user

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html", title="OraJobs | Home")

@main.route("/about-us")
def about():
    return render_template("about.html", title="OraJobs | About Us")

@main.route("/logout")
def logout():
    logout_user()
    flash(f'Logged Out successfully.', 'info')
    return redirect(url_for('.home'))
