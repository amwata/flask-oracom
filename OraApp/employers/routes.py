
from flask import render_template, Blueprint, url_for, flash, redirect, request, abort
from OraApp import db, bcrypt
from OraApp.forms import User_Login, Employer_Signup, Employer_User_Update, Job_Add, Job_Update, Forgot_Password, Reset_Password, Company_Search
from OraApp.models import User, Employer, Job, jobs_applied, Applicant
from OraApp.utils import save_file, user_role_required, remove_file, send_pwd_reset_email, send_shortlist_email
from flask_login import login_user, current_user

employer = Blueprint('employer', __name__)

# Employer dashboard
@employer.route("/employer/account/")
@user_role_required('employer')
def employer_account():
    user = current_user.employers
    job_posts = user.jobs
    applicants = db.session.query(Applicant).select_from(Applicant).join(jobs_applied).join(Job).filter_by(company=user).all()
    listed = db.session.query(Applicant).select_from(Applicant).join(jobs_applied).filter_by(shortlisted=True).join(Job).filter_by(company=user).all() 

    return render_template("employers/account.html", title="Employer | Account", jobs=job_posts, applicants=applicants, listed=listed)

# Employer/company details
@employer.route("/company/<int:company_id>/profile/")
def profile(company_id):
    company = Employer.query.get_or_404(company_id)
    return render_template("employers/profile.html", title="OraJobs | Company Profile", company=company)

# company list
@employer.route("/companies/")
@employer.route("/company/list/")
def company_list():
    form1 = Company_Search()
    page = request.args.get('page', 1, type=int)
    companies = Employer.query.paginate(page=page, per_page=15)
    head = 'List of Companies'
    return render_template("employers/list.html", title="OraJobs | Companies", companies=companies, head=head, form1=form1)

@employer.route("/employer/jobs/<int:job_id>/details/")
@user_role_required('employer')
def job_details(job_id):
    job = Job.query.get_or_404(job_id)
    if not job.company == current_user.employers:
        abort(403)
    applicants = db.session.query(jobs_applied.c.job_id).filter_by(job_id=job_id).all()

    return render_template("employers/job-details.html", title="OraJobs | Job Details", job=job, applicants=applicants)

@employer.route("/employer/posted-jobs")
@user_role_required('employer')
def posted_jobs():
    user = current_user.employers
    page = request.args.get('page', 1, type=int)
    jobs = Job.query.filter_by(company=user).order_by(Job.date_posted.desc()).paginate(page=page, per_page=15)
    list = db.session.query(jobs_applied.c.job_id, jobs_applied.c.applicant_id, jobs_applied.c.shortlisted)

    return render_template("employers/jobs.html", title="OraJobs | Posted Jobs", jobs=jobs, list=list)

# Jobs posting
@employer.route("/employer/post-jobs/", methods=['GET', 'POST'])
@user_role_required('employer')
def post_jobs():
    user = current_user.employers
    form = Job_Add()
    form.company_id.data = user.id
    if form.validate_on_submit():
        salary = form.salary.data if form.salary.data else 0
        job = Job(title=form.title.data.strip(), category=form.category.data, type=form.type.data, description=form.description.data, salary=salary, company=user)
        db.session.add(job)
        db.session.commit()
        
        flash(f'New Job Added Successfully!', 'success')
        return redirect(url_for('.posted_jobs'))
    h = 'New Job'
    return render_template("employers/post_jobs.html", title="Employer | Post Jobs", form=form, h=h)

@employer.route("/employer/jobs/<int:job_id>/update", methods=['GET', 'POST'])
@user_role_required('employer')
def edit_jobs(job_id):
    job = Job.query.get_or_404(job_id)

    if not job.company == current_user.employers:
        abort(403)

    form = Job_Update()
    if form.validate_on_submit():
        job.title = form.title.data.strip()
        job.category = form.category.data.strip()
        job.type = form.type.data 
        job.description = form.description.data
        job.salary = form.salary.data if form.salary.data else 0

        db.session.commit()
        flash(f'Job Updated Successfully.', 'success')
        return redirect(url_for('.posted_jobs'))
  
    form.title.data = job.title 
    form.category.data = job.category
    form.salary.data = job.salary
    form.type.data = job.type
    form.description.data = job.description
    h = 'Update Job'
    return render_template("employers/post_jobs.html", title="Employer | Update Job", form=form, job=job, h=h)

@employer.route("/employer/<int:job_id>/remove-job/", methods=['POST'])
@user_role_required('employer')
def remove_job(job_id):
    job = Job.query.get_or_404(job_id)
    if not job.company == current_user.employers:
        abort(403)

    db.session.delete(job)
    db.session.commit()
            
    flash(f'Job Removed Successfully!', 'success')
    return redirect(url_for('.posted_jobs'))

@employer.route("/employer/applicants/")
@user_role_required('employer')
def applicants():
    user = current_user.employers
    page = request.args.get('page', 1, type=int)

    query = db.session.query(Applicant, Job, jobs_applied.c.shortlisted, jobs_applied.c.date_applied).select_from(Applicant).join(jobs_applied).order_by(jobs_applied.c.date_applied).join(Job).filter_by(company=user).paginate(page=page, per_page=15)

    return render_template("employers/candidates.html", title="Employer | Applicants", applicants=query)

@employer.route("/employer/applicants/<int:job_id>")
@user_role_required('employer')
def applicants_per_job(job_id):
    job = Job.query.get_or_404(job_id)
    page = request.args.get('page', 1, type=int)
    if not job.company == current_user.employers:
        abort(403)
    applicants = db.session.query(Applicant, jobs_applied.c.shortlisted, jobs_applied.c.date_applied).select_from(Applicant).join(jobs_applied).filter_by(job_id=job_id).join(Job).order_by(jobs_applied.c.date_applied).all()

    return render_template("employers/filtered.html", title="OraJobs | Applicants per Job", applicants=applicants, job=job)

@employer.route("/employer/applicants/shortlisted")
@user_role_required('employer')
def listed_applicants():
    user = current_user.employers
    page = request.args.get('page', 1, type=int)

    query = db.session.query(Applicant, Job).select_from(Applicant).join(jobs_applied).filter_by(shortlisted=True).join(Job).filter_by(company=user).paginate(page=page, per_page=15)

    return render_template("employers/listed.html", title="Employer | Shortlists", applicants=query)

@employer.route("/employer/candidates/")
@user_role_required('employer')
def candidates():
    pass

# Sending emails to shortlisted applicants
@employer.route("/employer/send-message/<int:applicant_id>", methods=['GET', 'POST'])
@user_role_required('employer')
def send_message(applicant_id):
    pass

# Listing candidates and Sending email notifications to shortlisted applicants
@employer.route("/employer/list-applicant/<int:job_id>/<int:applicant_id>")
@user_role_required('employer')
def list_applicant(job_id, applicant_id):
    user = current_user.employers
    job = Job.query.get_or_404(job_id)
    applicant = Applicant.query.filter_by(id=applicant_id).first()
    email=User.query.filter_by(id=applicant.user_id).first().email
    if not job.company == user:
        abort(403)

    db.session.query(jobs_applied).filter((jobs_applied.c.job_id==job_id)&(jobs_applied.c.applicant_id==applicant_id)).update(dict(shortlisted = True))
    list = db.session.query(Job, Applicant, jobs_applied.c.date_applied).select_from(Job).join(jobs_applied).join(Applicant).filter((jobs_applied.c.job_id==job_id)&(jobs_applied.c.applicant_id==applicant_id)).first()

    try:
        send_shortlist_email(email, dict(list))
        db.session.commit()

        flash(' Applicant listed Successfully', 'success')
        return redirect(url_for('.listed_applicants'))
    except:
        flash('Something went wrong! Please Try Again.', 'warning')
        return redirect(url_for('.applicants'))

@employer.route("/employer/list-applicant/<int:job_id>/<int:applicant_id>",  methods=['POST'])
@user_role_required('employer')
def unlist_applicant(job_id, applicant_id):
    user = current_user.employers
    job = Job.query.get_or_404(job_id)
    if not job.company == user:
        abort(403)

    db.session.query(jobs_applied).filter((jobs_applied.c.job_id==job_id)&(jobs_applied.c.applicant_id==applicant_id)).update(dict(shortlisted = False))
    db.session.commit()
    flash('Applicant removed from your list Successfully', 'success')

    return redirect(url_for('.listed_applicants'))

@employer.route("/employer/notifications/")
@user_role_required('employer')
def notifications():
    pass

# employer account settings
@employer.route("/employer/settings/", methods=['GET', 'POST'])
@user_role_required('employer')
def settings():
    user = current_user.employers
    form = Employer_User_Update()

    if form.validate_on_submit():
        user.name = form.name.data.strip().upper()
        user.user.email = form.email.data.lower()
        user.phone = form.phone.data 
        user.location = form.location.data 
        user.tagline = form.tagline.data 
        user.description = form.description.data 
        user.website = form.website.data 

        if form.logo.data:
            new_file = save_file('employer/logo/', form.logo.data)
            if new_file:
                if user.logo != 'company.png':
                    old_file = f'employer/logo/{str(user.logo)}'
                    remove_file(old_file)
                
                user.logo = new_file

        db.session.commit()
        flash(f'Account Updated Successfully.', 'success')
        return redirect(url_for('.settings'))
  
    form.name.data = user.name 
    form.email.data = user.user.email
    form.phone.data = user.phone
    form.location.data = user.location
    form.tagline.data = user.tagline
    form.description.data = user.description
    form.website.data = user.website

    return render_template("employers/settings.html", title="OraJobs | Employer Settings", form=form, user = user)

@employer.route("/employer/<int:employer_id>/delete-logo", methods=['POST'])
@user_role_required('employer')
def delete_image(employer_id):
    user = Employer.query.get_or_404(employer_id)
    if not user.user == current_user:
        abort(403)

    if user.logo and user.logo != "company.png":
        file = f'employer/logo/{str(user.logo)}'
        try:
            remove_file(file)
            user.logo = 'company.png'
            db.session.commit()
            flash(f'Logo Removed Successfully!', category='success')
        except FileNotFoundError:
            user.logo = 'company.png'
            db.session.commit()
            flash(f'File not Found!', category='danger')
    
    return redirect(url_for('.settings'))

# employer account sign in
@employer.route("/employer/login/", methods=['GET', 'POST'])
def employer_login():
    if current_user.is_authenticated and current_user.employers:
        return redirect(url_for('.employer_account'))
    form = User_Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.employers and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Login successs.', 'info')

            return redirect(request.args.get('next') or url_for('.employer_account'))
        else:
            flash(f'Invalid Email or Password! Please Try Again.', 'danger')
    return render_template("employers/login.html", title="OraJobs | Employer Login", form=form)

# employer registration
@employer.route("/employer/signup/", methods=['GET', 'POST'])
def employer_signup():
    if current_user.is_authenticated and current_user.employers:
        return redirect(url_for('.employer_account'))
    form = Employer_Signup()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(email=form.email.data.lower(), user_role='employer', password=pw_hash)
        db.session.add(user)

        if form.logo.data:
            logo = save_file('employer/logo/', form.logo.data) 
            employer = Employer(name=form.name.data.strip().upper(), location=form.location.data.strip().capitalize(), phone=form.phone.data, tagline=form.tagline.data, description=form.description.data, website=form.website.data, logo=logo, user=user)
            db.session.add(employer)
            db.session.commit()
        else:
            employer = Employer(name=form.name.data.strip().upper(), location=form.location.data.strip().capitalize(), phone=form.phone.data, tagline=form.tagline.data, description=form.description.data, website=form.website.data, user=user)
            db.session.add(employer)
            db.session.commit()

        flash(f'Account Successfully created for {form.email.data}!', 'success')
        login_user(user, remember=True)
        return redirect(url_for('.employer_account'))        
    return render_template("employers/signup.html", title="OraJobs | Employer Signup", form=form)

# Employer User password reset request
@employer.route("/employer/password-reset", methods=['GET', 'POST'])
def password_reset_request():
    if current_user.is_authenticated and current_user.employers:
        return redirect(url_for('.employer_account'))
    form = Forgot_Password()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            try:
                send_pwd_reset_email(user, 'employer', user.employers.name)
                flash('A password reset link has been sent to your email', 'info')
                return redirect(url_for('.employer_login'))
            except:
                flash('Something went wrong! Please Try Again.', 'warning')
                return redirect(url_for('.password_reset_request'))
        else:
            flash('Email not registered. Send the email you registered your account with.', 'warning')
            return redirect(url_for('.password_reset_request'))
    return render_template("forgot_password.html", title="Employer | Reset Password", form=form)

# Employer user password reset token
@employer.route("/employer/password-reset/<string:token>", methods=['GET', 'POST'])
def password_reset_link(token):
    if current_user.is_authenticated and current_user.employers:
        return redirect(url_for('.employer_account'))
    user = User.verify_reset_token(token)
    if not user:
        flash('The link is either invalid or has expired!', 'warning')
        return redirect(url_for('.password_reset_request'))
          
    form = Reset_Password()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = pw_hash
        db.session.commit()

        flash('Your Password has been updated', 'success')
        return redirect(url_for('.employer_login'))
    
    return render_template("reset_password.html", title="Employer | Reset Password", form=form)

# Company search
@employer.route("/company/search", methods=['POST'])
def company_search():
    form1 = Company_Search()
    form = request.form
    name_or_location = form['name']
    search = "%{0}%".format(name_or_location)

    page = request.args.get('page', 1, type=int)
    companies = Employer.query.filter((Employer.name.like(search) | Employer.location.like(search))).order_by(Employer.name.desc()).paginate(page=page, per_page=15) 
    
    head = f'Search Results for "{name_or_location}": {companies.total}'
    return render_template("employers/list.html", title="OraJobs | Company Search", companies=companies, head=head, form1=form1)
