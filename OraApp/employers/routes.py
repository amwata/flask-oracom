
from flask import render_template, Blueprint, url_for, flash, redirect, request
from OraApp import db, bcrypt
from OraApp.forms import User_Login, Employer_Signup
from OraApp.models import User, Employer 
from OraApp.utils import save_file, user_role_required
from flask_login import login_user, current_user

employer = Blueprint('employer', __name__)

# @employer.route("/employer")
@employer.route("/employer/account")
@user_role_required('employer')
def employer_account():
    return "<h1>Employer account<h1>"

@employer.route("/companies")
@employer.route("/company/list")
def company_list():
    return "<h1>Companies List<h1>"

@employer.route("/employer/profile")
def employer_profile():
    return "<h1>Employer profile<?h1>"

@employer.route("/employer/login", methods=['GET', 'POST'])
def employer_login():
    if current_user.is_authenticated and current_user.user_role == 'employer':
        return redirect(url_for('.employer_account'))
    form = User_Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.user_role == 'employer' and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Login successs.', 'info')

            return redirect(request.args.get('next') or url_for('.employer_account'))
        else:
            flash(f'Invalid Email or Password! Please Try Again.', 'danger')
    return render_template("employers/login.html", title="OraJobs | Employer Login", form=form)


@employer.route("/employer/signup", methods=['GET', 'POST'])
def employer_signup():
    if current_user.is_authenticated and current_user.user_role == 'employer':
        return redirect(url_for('.employer_account'))
    form = Employer_Signup()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(email=form.email.data, user_role='employer', password=pw_hash)
        db.session.add(user)

        if form.logo.data:
            logo = save_file('employer/logo/', form.logo.data) 
            employer = Employer(name=form.name.data.strip().upper(), location=form.location.data.strip().capitalize(), phone=form.phone.data, tagline=form.tagline.data, description=form.description.data, website=form.website.data, logo=logo, employer=user)
            db.session.add(employer)
            db.session.commit()
        else:
            employer = Employer(name=form.name.data.strip().upper(), location=form.location.data.strip().capitalize(), phone=form.phone.data, tagline=form.tagline.data, description=form.description.data, website=form.website.data, employer=user)
            db.session.add(employer)
            db.session.commit()

        flash(f'Account Successfully created for {form.email.data}!', 'success')
        login_user(user, remember=True)
        return redirect(url_for('.employer_account'))        
    return render_template("employers/signup.html", title="OraJobs | Employer Signup", form=form)


