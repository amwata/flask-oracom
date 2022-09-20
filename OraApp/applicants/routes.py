
from flask import render_template, Blueprint, url_for, flash, redirect, request, abort
from OraApp import db, bcrypt
from OraApp.forms import Applicant_User_Update, User_Login, Applicant_Signup, Applicant_User_Update
from OraApp.models import User, Applicant, Job, jobs_applied
from OraApp.utils import save_file, remove_file, user_role_required
from flask_login import login_user, current_user


applicant = Blueprint('applicant', __name__)

@applicant.route("/applicant/account")
@user_role_required('applicant')
def applicant_account():
    user = current_user.applicants
    return render_template("applicants/account.html", title="Applicant | Account", user=user)

@applicant.route("/applicant/settings", methods=['GET','POST'])
@user_role_required('applicant')
def settings():
    user = current_user.applicants
    form = Applicant_User_Update()

    if form.validate_on_submit():
        user.f_name = form.f_name.data.strip().capitalize()
        user.l_name = form.l_name.data.strip().capitalize()
        user.user.email = form.email.data.lower()
        user.phone = form.phone.data 

        if form.resume.data:
            new_file = save_file('applicant/resume/', form.resume.data)
            if new_file:
                old_file = f'applicant/resume/{str(user.resume)}'
                try:
                    remove_file(old_file)
                except FileNotFoundError:
                    flash(f'File or Directory not found!', 'danger')
                user.resume = new_file

        if form.image.data:
            img = save_file('applicant/image/', form.image.data)
            if img:
                if user.image != 'anony.png':
                    file = f'applicant/image/{str(user.image)}'
                    remove_file(file)
                user.image = img

        db.session.commit()
        flash(f'Account Updated Successfully.', 'success')
        return redirect(url_for('.settings'))

    form.f_name.data = user.f_name 
    form.l_name.data = user.l_name
    form.email.data = user.user.email
    form.phone.data = user.phone

    return render_template("applicants/settings.html", title="OraJobs | Applicant Settings", form=form, user = user)


@applicant.route("/applicant/jobs-applied")
@user_role_required('applicant')
def jobs_applied():
    user = current_user.applicants
    page = request.args.get('page', 1, type=int)
    # jobs = Job.query.filter_by(company=user).order_by(Job.date_posted.desc()).paginate(page=page, per_page=15)
    jobs = Job.query.all()

    # applied = Applicant.query.join(Job).all()
    # .join(Job).filter((jobs_applied.c.applicant_id == Applicant.id) & (jobs_applied.c.job_id == Job.id)).all()
    # flash(f'{applied}', 'primary')

    # jobs = db.session.query(Job, jobs_applied, Applicant).select_from(Job).join(jobs_applied).join(Applicant).filter(Applicant.id==3).all()
    # applied_jobs = db.session.query(Job).select_from(Job).join(jobs_applied).join(Applicant).filter(Applicant.id==user.id).paginate(page=page, per_page=1)
    applications = db.session.query(jobs_applied).filter_by(applicant_id=user.id).all()

    return render_template("applicants/jobs.html", title="OraJobs | Applied Jobs", jobs=jobs)

@applicant.route("/applicant/application/<int:job_id>", methods=['GET','POST'])
@user_role_required('applicant')
def apply_for_job(job_id):
    user = current_user.applicants
    job = Job.query.get_or_404(job_id)
    
    user.applied_jobs.append(job)
    db.session.commit()

    flash(f'Application sent Successfully!', 'success')
    return redirect(url_for('.jobs_applied'))

@applicant.route("/applicant/<int:applicant_id>/delete-image", methods=['POST'])
@user_role_required('applicant')
def delete_image(applicant_id):
    user = Applicant.query.get_or_404(applicant_id)
    if not user.user == current_user:
        abort(403)

    if user.image and user.image != "anony.png":
        file = f'applicant/image/{str(user.image)}'
        try:
            remove_file(file)
            user.image = 'anony.png'
            db.session.commit()
            flash(f'Image Removed Successfully!', category='success')
        except FileNotFoundError:
            user.image = 'anony.png'
            db.session.commit()
            flash(f'File not Found!', category='danger')
    
    return redirect(url_for('.settings'))

@applicant.route("/applicant/notifications")
@user_role_required('applicant')
def notifications():
    pass


@applicant.route("/applicant/login", methods=['GET', 'POST'])
def applicant_login():
    if current_user.is_authenticated and current_user.applicants:
        return redirect(url_for('.applicant_account'))
    form = User_Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.applicants and bcrypt.check_password_hash(user.password, form.password.data):
            match = Applicant.query.filter_by(user_id=user.id).first()
            login_user(user, remember=form.remember.data)
            flash(f'Logged in as {match.l_name}!', 'success')
            return redirect(request.args.get('next') or url_for('.applicant_account'))
        else:
            flash(f'Invalid Email or Password! Please Try Again.', 'danger')
    return render_template("applicants/login.html", title="OraJobs | Applicant Login", form=form)

@applicant.route("/applicant/signup", methods=['POST', 'GET'])
def applicant_signup():
    if current_user.is_authenticated and current_user.applicants:
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

