from flask import render_template, Blueprint, url_for, flash, redirect
from OraApp import db, bcrypt
from OraApp.forms import User_Login, Applicant_Signup
from OraApp.models import Applicant 
from flask_login import login_user, current_user, logout_user

applicant = Blueprint('applicant', __name__)

@applicant.route("/applicant")
@applicant.route("/applicant/dashboard")
def applicant_dashboard():
    return render_template("applicants/dashboard.html", title="OraJobs | Applicant Dashboard")

@applicant.route("/applicant/profile")
@applicant.route("/applicant/profile/<name>")
def applicant_profile(name):
    return f"<h1>Applicant profile<br>{name}<?h1>"

@applicant.route("/applicant/login", methods=['GET', 'POST'])
def applicant_login():
    if current_user.is_authenticated:
        return redirect(url_for('.applicant_dashboard'))
    form = User_Login()
    if form.validate_on_submit():
        user = Applicant.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('.applicant_dashboard'))
        else:
            flash(f'Invalid Email or Password! Please Try Again.', 'danger')
    return render_template("applicants/login.html", title="OraJobs | Applicant Login", form=form)

@applicant.route("/applicant/signup", methods=['POST', 'GET'])
def applicant_signup():
    if current_user.is_authenticated:
        return redirect(url_for('.applicant_dashboard'))
    form = Applicant_Signup()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        applicant = Applicant(f_name=form.f_name.data, l_name=form.l_name.data, email=form.email.data, phone=form.phone.data, resume=form.resume.data, image=form.image.data, password=pw_hash)
        db.session.add(applicant)
        db.session.commit()

        flash(f'Account Successfully created for {form.email.data}!', 'success')
        login_user(applicant, remember=True)
        return redirect(url_for('.applicant_dashboard', name=form.l_name.data))
    return render_template("applicants/signup.html", title="OraJobs | Applicant Signup", form=form)

