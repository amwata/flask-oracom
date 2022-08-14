from flask import render_template, Blueprint

employer = Blueprint('employer', __name__)

@employer.route("/employer")
@employer.route("/employer/dashboard")
def employer_dashboard():
    return "<h1>Employer dashboard<?h1>"

@employer.route("/employer/profile")
def employer_profile():
    return "<h1>Employer profile<?h1>"

@employer.route("/employer/login")
def employer_login():
    return "<h1>Employer sign in<?h1>"

@employer.route("/employer/logout")
def employer_logout():
    return "<h1>Employer log out<?h1>"

