from flask import render_template
from app import app

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html", title="OraJobs | Home")

@app.route("/about-us")
def about():
    return render_template("about.html", title="OraJobs | About Us")

@app.route("/jobs-list")
def jobs():
    return render_template("jobs.html", title="OraJobs | Jobs")