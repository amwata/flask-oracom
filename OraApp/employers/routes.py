from flask import render_template, Blueprint, url_for, flash, redirect
from OraApp.forms import Employer_Signup, User_Login, Applicant_Signup

employer = Blueprint('employer', __name__)

@employer.route("/employer")
@employer.route("/employer/account")
def employer_account():
    return "<h1>Employer account<?h1>"

@employer.route("/employer/profile")
def employer_profile():
    return "<h1>Employer profile<?h1>"

@employer.route("/employer/login", methods=['GET', 'POST'])
def employer_login():
    form = User_Login()
    if form.validate_on_submit():
        flash(f'Login Successful for {form.email.data}!', 'success')
        return redirect(url_for('main.home'))
        
    return render_template("employers/login.html", title="OraJobs | Employer Login", form=form)


@employer.route("/employer/signup", methods=['GET', 'POST'])
def employer_signup():
    form = Employer_Signup()
    if form.validate_on_submit():
        flash(f'Login Successful for {form.email.data}!', 'success')
        return redirect(url_for('main.home'))
        
    return render_template("employers/signup.html", title="OraJobs | Employer Signup", form=form)


