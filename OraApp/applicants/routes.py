from flask import render_template, Blueprint

applicant = Blueprint('applicant', __name__)


@applicant.route("/applicant")
@applicant.route("/applicant/dashboard")
def applicant_dashboard():
    return "<h1>applicant dashboard<br><?h1>"

@applicant.route("/applicant/profile")
@applicant.route("/applicant/profile/<name>")
def applicant_profile(name):
    return f"<h1>Applicant profile<br>{name}<?h1>"

@applicant.route("/applicant/login")
def applicant_login():
    return render_template("applicants/login.html", title="OraJobs | Applicant Login")

@applicant.route("/applicant/register")
def applicant_signup():
    return render_template("applicants/signup.html", title="OraJobs | Applicant Registration")