from flask import render_template, Blueprint

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template("index.html", title="OraJobs | Home")

@main.route("/about-us")
def about():
    return render_template("about.html", title="OraJobs | About Us")


