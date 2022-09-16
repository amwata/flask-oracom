
from flask import render_template, Blueprint, url_for, flash, redirect, request
from OraApp import db, bcrypt
from OraApp.forms import User_Login, Applicant_Signup, Applicant_Update
from OraApp.models import User, Applicant 
from OraApp.utils import save_file, user_role_required
from flask_login import login_user, current_user


applicant = Blueprint('applicant', __name__)

@applicant.route("/applicant/account")
@user_role_required('applicant')
def applicant_account():
    pass

@applicant.route("/applicant/settings")
@user_role_required('applicant')
def settings():
    user = Applicant.query.filter_by(user_id=current_user.id).first()
    form = Applicant_Update()

    # if form.validate_on_submit():
    #     user.name = form.name.data.strip().capitalize()
    #     current_user.email = form.email.data.lower()
    #     user.phone = form.phone.data 
    #     if form.image.data:
    #         img = save_file('admin/image/', form.image.data)
    #         if img:
    #             if user.image != 'anony.png':
    #                 file = f'admin/image/{str(user.image)}'
    #                 remove_file(file)
    #             user.image = img

        # db.session.commit()
        # flash(f'Information Updated Successfully.', 'success')
        # return redirect(url_for('.admin_settings'))

    form.f_name.data = user.f_name 
    form.l_name.data = user.l_name
    form.email.data = user.user.email
    form.phone.data = user.phone

    return render_template("applicants/settings.html", title="OraJobs | Applicant account", form=form, user = user)

@applicant.route("/applicant/jobs-applied")
@user_role_required('applicant')
def jobs_applied():
    pass

@applicant.route("/applicant/notifications")
@user_role_required('applicant')
def notifications():
    pass


@applicant.route("/applicant/login", methods=['GET', 'POST'])
def applicant_login():
    if current_user.is_authenticated and current_user.user_role == 'applicant':
        return redirect(url_for('.applicant_account'))
    form = User_Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.user_role == 'applicant' and bcrypt.check_password_hash(user.password, form.password.data):
            match = Applicant.query.filter_by(user_id=user.id).first()
            login_user(user, remember=form.remember.data)
            flash(f'Logged in as {match.l_name}!', 'success')
            return redirect(request.args.get('next') or url_for('.applicant_account'))
        else:
            flash(f'Invalid Email or Password! Please Try Again.', 'danger')
    return render_template("applicants/login.html", title="OraJobs | Applicant Login", form=form)

@applicant.route("/applicant/signup", methods=['POST', 'GET'])
def applicant_signup():
    if current_user.is_authenticated and current_user.user_role == 'applicant':
        return redirect(url_for('.applicant_account'))
    form = Applicant_Signup()
    if form.validate_on_submit():
        resume = save_file('applicant/resume/', form.resume.data)
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(email=form.email.data.lower(), user_role='applicant', password=pw_hash)
        db.session.add(user)

        if form.image.data:
            image = save_file('applicant/image/', form.image.data) 
            applicant = Applicant(f_name=form.f_name.data.strip().capitalize(), l_name=form.l_name.data.strip().capitalize(), phone=form.phone.data, resume=resume, image=image, user=user)
            db.session.add(applicant)
            db.session.commit()
        else:
            applicant = Applicant(f_name=form.f_name.data.strip().capitalize(), l_name=form.l_name.data.strip().capitalize(), phone=form.phone.data, resume=resume, user=user)
            db.session.add(applicant)
            db.session.commit()

        flash(f'Account Successfully created for {form.email.data}!', 'success')
        login_user(user, remember=True)
        return redirect(url_for('.settings'))
    return render_template("applicants/signup.html", title="OraJobs | Applicant Signup", form=form)

