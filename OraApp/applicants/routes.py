from urllib import request
from flask import render_template, Blueprint, url_for, flash, redirect, request
from OraApp import db, bcrypt, login_manager
from OraApp.forms import User_Login, Applicant_Signup
from OraApp.models import Applicant 
from flask_login import login_user, current_user, login_required

login_manager.login_view = '.applicant_login'
login_manager.login_message_category = 'info'

applicant = Blueprint('applicant', __name__)

@applicant.route("/applicant")
@applicant.route("/applicant/account")
@login_required
def applicant_account():
    image = url_for('static', filename='applicant/image/' + str(current_user.id))
    return render_template("applicants/account.html", title="OraJobs | Applicant account", image = image)

@applicant.route("/applicant/profile")
@applicant.route("/applicant/profile/<name>")
def applicant_profile(name):
    return f"<h1>Applicant profile<br>{name}<?h1>"

@applicant.route("/applicant/login", methods=['GET', 'POST'])
def applicant_login():
    if current_user.is_authenticated:
        return redirect(url_for('.applicant_account'))
    form = User_Login()
    if form.validate_on_submit():
        user = Applicant.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('.applicant_account'))
        else:
            flash(f'Invalid Email or Password! Please Try Again.', 'danger')
    return render_template("applicants/login.html", title="OraJobs | Applicant Login", form=form)

@applicant.route("/applicant/signup", methods=['POST', 'GET'])
def applicant_signup():
    if current_user.is_authenticated:
        return redirect(url_for('.applicant_account'))
    form = Applicant_Signup()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        applicant = Applicant(f_name=form.f_name.data, l_name=form.l_name.data, email=form.email.data, phone=form.phone.data, resume=form.resume.data, image=form.image.data, password=pw_hash)
        db.session.add(applicant)
        db.session.commit()

        flash(f'Account Successfully created for {form.email.data}!', 'success')
        login_user(applicant, remember=True)
        return redirect(url_for('.applicant_account'))
    return render_template("applicants/signup.html", title="OraJobs | Applicant Signup", form=form)

