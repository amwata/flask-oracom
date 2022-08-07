from flask import render_template
from app import app

@app.route("/applicant")
@app.route("/applicant/dashboard")
def applicant():
    return "<h1>applicant dashboard<br><?h1>"

@app.route("/applicant/profile")
@app.route("/applicant/profile/<name>")
def applicantProfile(name):
    return f"<h1>Applicant profile<br>{name}<?h1>"

@app.route("/applicant/login")
def applicantLogin():
    return render_template("applicant-log-in.html", title="OraJobs | Applicant Login")

@app.route("/applicant/logout")
def applicantLogout():
    return "<h1>Applicant log out<?h1>"