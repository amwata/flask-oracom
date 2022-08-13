from flask import render_template
from app import app

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", title="OraJobs | Home")

@app.route("/about-us")
def about():
    return render_template("about.html", title="OraJobs | About Us")


