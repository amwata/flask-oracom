
from flask import render_template, Blueprint, url_for, flash, redirect, request, abort, make_response
from OraApp import db, bcrypt
from OraApp.forms import Applicant_Add, Applicant_Update, Employer_Add, Employer_Update, User_Login, Admin_Update, Admins_Add, Admins_Edit, Job_Add, Job_Update, Forgot_Password, Reset_Password
from OraApp.models import Admin, User, Job, Employer, Applicant, jobs_applied
from OraApp.utils import user_role_required, save_file, remove_file, send_pwd_reset_email
from flask_login import login_user, current_user
import pdfkit


admin = Blueprint('admin', __name__)

# admin dashboard
@admin.route("/admin/dashboard/")
@user_role_required('admin')
def admin_account():
    user = current_user.admins
    jobs = len(Job.query.all())
    employers = len(Employer.query.all())
    applicants = len(Applicant.query.all())
    applied = len(db.session.query(jobs_applied).all())

    query = db.session.query(Job.category.distinct().label("category"))
    categories = [row.category for row in query.all()]

    dash = {'jobs': jobs, 'employers': employers, 'applicants': applicants, 'jobs_applied': applied, 'categories': len(categories)}
    return render_template("admin/dashboard.html", title="Admin | Dashboard", user=user, dash=dash )

@admin.route("/admin/job-categories/")
@user_role_required('admin')
def admin_job_categories():
    user = current_user.admins
    page = request.args.get('page', 1, type=int)
    query = db.session.query(Job.category.distinct().label('category')).paginate(page=page, per_page=15)
    jobs = Job.query
    categories = [row.category for row in query.items]
    
    return render_template("admin/categories.html", title="Admin | Job Categories", user=user, jobs=jobs, categories=categories,pages=query)

@admin.route("/admin/jobs-list/")
@user_role_required('admin')
def admin_jobs():
    user = current_user.admins
    jobs = Job.query.all()
    return render_template("admin/jobs.html", title="Admin | Jobs List", user=user, jobs=jobs)

@admin.route("/admin/job-categories/<string:category>")
@user_role_required('admin')
def admin_filtered_jobs(category):
    user = current_user.admins
    jobs = Job.query.filter_by(category=category).all() or abort(404)
    head = f'Jobs in {category}: {len(jobs)}'
    return render_template("admin/jobs.html", title="Admin | Jobs List", user=user, jobs=jobs, head=head)

@admin.route("/admin/jobs-applied/")
@user_role_required('admin')
def admin_jobs_applied():
    user = current_user.admins
    jobs = db.session.query(Job, Applicant, jobs_applied.c.date_applied, jobs_applied.c.shortlisted).select_from(Job).join(jobs_applied).join(Applicant).order_by(jobs_applied.c.date_applied.desc()).all()

    return render_template("admin/jobs_applied.html", title="OraJobs | Applied Jobs", jobs=jobs, user=user)

@admin.route("/admin/jobs/new-job/", methods=['GET', 'POST'])
@user_role_required('admin')
def admin_job_add():
    user = current_user.admins
    form = Job_Add()
    if form.validate_on_submit():
        company = Employer.query.filter_by(id=form.company_id.data).first()
        if company:    
            salary = form.salary.data if form.salary.data else 0
            job = Job(title=form.title.data.strip(), category=form.category.data, type=form.type.data, description=form.description.data, salary=salary, company=company)
            db.session.add(job)
            db.session.commit()
            
            flash(f'New Job Added Successfully!', 'success')
            return redirect(url_for('.admin_jobs'))
        else:
            flash(f'Company does not exist!', 'danger')
    return render_template("admin/new_jobs.html", title="Admin | Add Job", user=user, form=form)

@admin.route("/admin/jobs/<int:job_id>/update-job/", methods=['GET', 'POST'])
@user_role_required('admin')
def admin_job_update(job_id):
    user = current_user.admins
    updated = Job.query.get_or_404(job_id)
    form = Job_Update()

    if form.validate_on_submit():
        updated.title = form.title.data.strip()
        updated.category = form.category.data.strip()
        updated.type = form.type.data 
        updated.description = form.description.data
        updated.salary = form.salary.data if form.salary.data else 0

        db.session.commit()
        flash(f'Job Updated Successfully.', 'success')
        return redirect(url_for('.admin_jobs'))
  
    form.title.data = updated.title 
    form.category.data = updated.category
    form.salary.data = updated.salary
    form.type.data = updated.type
    form.description.data = updated.description
    
    return render_template("admin/update_jobs.html", title="Admin | Update Job", form=form, user=user, updated=updated)

@admin.route("/admin/<int:job_id>/remove-job/", methods=['POST'])
@user_role_required('admin')
def admin_job_remove(job_id):
    job = Job.query.get_or_404(job_id)

    db.session.delete(job)
    db.session.commit()
            
    flash(f'Job Removed Successfully!', 'success')
    return redirect(url_for('.admin_jobs'))

# reports page
@admin.route("/admin/reports/")
@user_role_required('admin')
def reports():
    user = current_user.admins

    locations = db.session.query(Employer.location.distinct()).all()
    companies = [Employer.query.all()]
    applicants = [Applicant.query.all()]
    jobs = [Job.query.all()]
    applications = [ sum([db.session.query(Applicant).all()], []) ]
    applied = [ sum([db.session.query(Job).select_from(Job).join(jobs_applied).join(Applicant).all()], []) ]
    listed = [ sum([db.session.query(Applicant).select_from(Job).join(jobs_applied).filter(jobs_applied.c.shortlisted == True).join(Applicant).all()], []) ]

    payload = {'locations': locations, 'companies': sum(companies, []), 'jobs': sum(jobs, []), 'applications': sum(applications, []), 'listed': sum(listed, []), 'applied': sum(applied, []), 'applicants': sum(applicants, [])}

    title1 = 'Summery Report on OraJobs'
    title2 = 'Report on Employers per Location'

    return render_template("admin/reports/index.html", title="Admin | Reports", user=user, payload=payload, title1=title1, title2=title2)

@admin.route("/admin/report/<string:report>")
@user_role_required('admin')
def filtered_report(report):
    if report == 'companies':
        user = current_user.admins
        users = Employer.query.all()
        title1 = 'Registered Employers'
        title2 = 'Report on Registered Employers'
        return render_template("admin/reports/companies_page.html", title="Admin | Employers Report", user=user, companies=users, title1=title1, title2=title2, filter=report)
    elif report == 'applicants':
        user = current_user.admins
        users = Applicant.query.all()
        title1 = 'Registered Applicants'
        title2 = 'Report on Registered Applicants'
        return render_template("admin/reports/applicants_page.html", title="Admin | Applicants Report", user=user, applicants=users, title1=title1, title2=title2, filter=report)
    elif report == 'jobs':
        user = current_user.admins
        jobs = Job.query.all()
        title1 = 'Posted Jobs'
        title2 = 'Report on Posted Jobs'
        return render_template("admin/reports/jobs_page.html", title="Admin | Jobs Report", user=user, jobs=jobs, title1=title1, title2=title2, filter=report)
    elif report == 'applications':
        user = current_user.admins
        applied = db.session.query(Job, Applicant, jobs_applied.c.date_applied, jobs_applied.c.shortlisted).select_from(Job).join(jobs_applied).join(Applicant).order_by(jobs_applied.c.date_applied.desc()).all()

        title1 = 'Jobs Applied'
        title2 = 'Report on Jobs Applied'
        return render_template("admin/reports/applications_page.html", title="Admin | Applications Report", user=user, applied=applied, title1=title1, title2=title2, filter=report)
    elif report == 'locations':
        user = current_user.admins
        locations = db.session.query(Employer.location.distinct()).all()
        companies = [ Employer.query.filter_by(location=str(c[0])).all() for c in locations]
        jobs = [ j[0].jobs for j in companies]
        applications = [ sum([db.session.query(Applicant).select_from(Job).join(jobs_applied).filter(jobs_applied.c.job_id==i.id).join(Applicant).all() for i in j], []) for j in jobs ]

        payload = {'locations': locations, 'companies': companies, 'jobs': jobs, 'applications': applications}

        title1 = 'Employers Location'
        title2 = 'Report on Employers per Location'
        return render_template("admin/reports/locations_page.html", title="Admin | Employers Locations Report", user=user, payload=payload, title1=title1, title2=title2, filter=report)
    else:
        abort(404)

@admin.route("/admin/print_report/<string:report>", methods=['POST'])
@user_role_required('admin')
def print_report(report):
    if report == 'companies':
        user = current_user.admins
        users = Employer.query.all()
        title1 = 'Registered Employers'
        title2 = 'Report on Registered Employers'
        rendered = render_template("admin/reports/companies_pdf.html", title="Admin | Employers Report", user=user, companies=users, title1=title1, title2=title2)
    elif report == 'applicants':
        user = current_user.admins
        users = Applicant.query.all()
        title1 = 'Registered Applicants'
        title2 = 'Report on Registered Applicants'
        rendered = render_template("admin/reports/applicants_pdf.html", title="Admin | Applicants Report", user=user, applicants=users, title1=title1, title2=title2)
    elif report == 'jobs':
        user = current_user.admins
        jobs = Job.query.all()
        title1 = 'Posted Jobs'
        title2 = 'Report on Posted Jobs'
        rendered = render_template("admin/reports/jobs_pdf.html", title="Admin | Jobs Report", user=user, jobs=jobs, title1=title1, title2=title2)
    elif report == 'applications':
        user = current_user.admins
        applied = db.session.query(Job, Applicant, jobs_applied.c.date_applied, jobs_applied.c.shortlisted).select_from(Job).join(jobs_applied).join(Applicant).order_by(jobs_applied.c.date_applied.desc()).all()
        
        list = db.session.query(Applicant, jobs_applied.c.shortlisted).select_from(Job).join(jobs_applied).join(Applicant).filter(jobs_applied.c.shortlisted).all()
        applicants = db.session.query(jobs_applied.c.applicant_id.distinct()).all()
        jobs = db.session.query(jobs_applied.c.job_id.distinct()).all()
        
        title1 = 'Jobs Applied'
        title2 = 'Report on Jobs Applied'
        rendered = render_template("admin/reports/applications_pdf.html", title="Admin | Applications Report", user=user, applied=applied, title1=title1, title2=title2, filter=report, list=list, applicants=applicants, jobs=jobs)
    elif report == 'locations':
        user = current_user.admins
        locations = db.session.query(Employer.location.distinct()).all()
        companies = [ Employer.query.filter_by(location=str(c[0])).all() for c in locations]
        jobs = [ j[0].jobs for j in companies]
        applications = [ sum([db.session.query(Applicant).select_from(Job).join(jobs_applied).filter(jobs_applied.c.job_id==i.id).join(Applicant).all() for i in j], []) for j in jobs ]

        payload = {'locations': locations, 'companies': companies, 'jobs': jobs, 'applications': applications}

        title1 = 'Employers Location'
        title2 = 'Report on Employers per Location'
        rendered = render_template("admin/reports/locations_pdf.html", title="Admin | Employers Locations Report", user=user, payload=payload, title1=title1, title2=title2, filter=report)
    elif report == 'summery':
        user = current_user.admins

        locations = db.session.query(Employer.location.distinct()).all()
        companies = [Employer.query.all()]
        applicants = [Applicant.query.all()]
        jobs = [Job.query.all()]
        applications = [ sum([db.session.query(Applicant).all()], []) ]
        applied = [ sum([db.session.query(Job).select_from(Job).join(jobs_applied).join(Applicant).all()], []) ]
        listed = [ sum([db.session.query(Applicant).select_from(Job).join(jobs_applied).filter(jobs_applied.c.shortlisted == True).join(Applicant).all()], []) ]

        payload = {'locations': locations, 'companies': sum(companies, []), 'jobs': sum(jobs, []), 'applications': sum(applications, []), 'listed': sum(listed, []), 'applied': sum(applied, []), 'applicants': sum(applicants, [])}

        title1 = 'Summery Report on OraJobs'
        title2 = 'Report on Employers per Location'

        rendered = render_template("admin/reports/summery_pdf.html", title="Admin | Reports", user=user, payload=payload, title1=title1, title2=title2)
    else:
        abort(404)
    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['content-Type'] = 'application/pdf'
    response.headers['content-Disposition'] = f'inline: filename={report}.pdf'
    return response

@admin.route("/admin/employers/")
@user_role_required('admin')
def admin_companies():
    user = current_user.admins
    users = Employer.query.all()
    return render_template("admin/employers.html", title="Admin | Manage Employers", user=user, companies=users)

@admin.route("/admin/employers/new-employer/", methods=['GET', 'POST'])
@user_role_required('admin')
def admin_company_add():
    user = current_user.admins
    form = Employer_Add()
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
        
        flash(f'New Employer Added Successfully!', 'success')
        return redirect(url_for('.admin_companies'))
    return render_template("admin/new_employers.html", title="Admin | Add Employer", user=user, form=form)

@admin.route("/admin/<int:company_id>/remove-employer/", methods=['POST'])
@user_role_required('admin')
def admin_company_remove(company_id):
    user = Employer.query.get_or_404(company_id)
    jobs = user.jobs

    Job.query.filter_by(company=user).delete()
         
    db.session.delete(user)
    db.session.delete(user.user)
    db.session.commit()

    if user.logo and user.logo != "company.png":
        file = f'employer/logo/{str(user.logo)}'
        try:
            remove_file(file)
        except FileNotFoundError:
            flash(f'File not Found!', category='danger')
            

    flash(f'Employer Removed Successfully!', 'success')
    return redirect(url_for('.admin_companies'))

@admin.route("/admin/employers/<int:company_id>/update-employer/", methods=['GET', 'POST'])
@user_role_required('admin')
def admin_company_update(company_id):
    user = current_user.admins
    updated = Employer.query.get_or_404(company_id)
    jobs = len(updated.jobs)
    form = Employer_Update()

    form.id.data = int(company_id)
    if form.validate_on_submit():
        updated.name = form.name.data.strip().upper()
        updated.user.email = form.email.data.lower()
        updated.phone = form.phone.data 
        updated.location = form.location.data 
        updated.tagline = form.tagline.data 
        updated.description = form.description.data 
        updated.website = form.website.data 

        if form.logo.data:
            new_file = save_file('employer/logo/', form.logo.data)
            if new_file:
                if updated.logo != 'company.png':
                    old_file = f'employer/logo/{str(updated.logo)}'
                    remove_file(old_file)
                
                updated.logo = new_file

        db.session.commit()
        flash(f'Employer Updated Successfully.', 'success')
        return redirect(url_for('.admin_companies'))
  
    form.name.data = updated.name 
    form.email.data = updated.user.email
    form.phone.data = updated.phone
    form.location.data = updated.location
    form.tagline.data = updated.tagline
    form.description.data = updated.description
    form.website.data = updated.website

    
    return render_template("admin/update_employers.html", title="Admin | Update Employer", form=form, user=user, jobs=jobs, updated=updated)

@admin.route("/admin/applicants/")
@user_role_required('admin')
def admin_applicants():
    user = current_user.admins
    users = Applicant.query.all()
    return render_template("admin/applicants.html", title="Admin | Manage Applicants", user=user, applicants=users)

@admin.route("/admin/applicants/new-applicant/", methods=['GET', 'POST'])
@user_role_required('admin')
def admin_applicant_add():
    user = current_user.admins
    form = Applicant_Add()
    if form.validate_on_submit():
        resume = save_file('applicant/resume/', form.resume.data)
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(email=form.email.data.lower(), user_role='applicant', password=pw_hash)
        db.session.add(user)
        
        applicant = Applicant(f_name=form.f_name.data.strip().capitalize(), l_name=form.l_name.data.strip().capitalize(), phone=form.phone.data, resume=resume, user=user)
        db.session.add(applicant)
        db.session.commit()
        
        flash(f'New Applicant Added Successfully!', 'success')
        return redirect(url_for('.admin_applicants'))
    return render_template("admin/new_applicants.html", title="Admin | Add Applicants", user=user, form=form)

@admin.route("/admin/<int:applicant_id>/remove-applicant/", methods=['POST'])
@user_role_required('admin')
def admin_applicant_remove(applicant_id):
    user = Applicant.query.get_or_404(applicant_id)

    db.session.delete(user)
    db.session.delete(user.user)
    db.session.commit()

    if user.resume:
        file = f'applicant/resume/{str(user.resume)}'
        try:
            remove_file(file)
        except FileNotFoundError:
            flash(f'File not Found!', category='danger')

    if user.image and user.image != "anony.png":
        file = f'applicant/image/{str(user.image)}'
        try:
            remove_file(file)
        except FileNotFoundError:
            flash(f'File not Found!', category='danger')
            

    flash(f'Applicant Removed Successfully!', 'success')
    return redirect(url_for('.admin_applicants'))

@admin.route("/admin/applicants/<int:applicant_id>/update-applicant/", methods=['GET', 'POST'])
@user_role_required('admin')
def admin_applicant_update(applicant_id):
    user = current_user.admins
    updated = Applicant.query.get_or_404(applicant_id)
    form = Applicant_Update()

    form.id.data = int(applicant_id)
    if form.validate_on_submit():
        updated.f_name = form.f_name.data.strip().capitalize()
        updated.l_name = form.l_name.data.strip().capitalize()
        updated.user.email = form.email.data.lower()
        updated.phone = form.phone.data 

        if form.resume.data:
            new_file = save_file('applicant/resume/', form.resume.data)
            if new_file:
                old_file = f'applicant/resume/{str(updated.resume)}'
                try:
                    remove_file(old_file)
                except FileNotFoundError:
                    flash(f'File or Directory not found!', 'danger')
                updated.resume = new_file

        db.session.commit()
        flash(f'Applicant Updated Successfully.', 'success')
        return redirect(url_for('.admin_applicants'))
  
    form.f_name.data = updated.f_name 
    form.l_name.data = updated.l_name
    form.email.data = updated.user.email
    form.phone.data = updated.phone
    
    return render_template("admin/update_applicants.html", title="Admin | Update Applicants", form=form, user=user, updated=updated)

@admin.route("/admin/settings/", methods=['GET', 'POST'])
@user_role_required('admin')
def admin_settings():
    user = current_user.admins
    admins = Admin.query.all()
    form = Admin_Update()

    if form.validate_on_submit():
        user.name = form.name.data.strip().capitalize()
        current_user.email = form.email.data.lower()
        user.phone = form.phone.data 
        if form.image.data:
            img = save_file('admin/image/', form.image.data)
            if img:
                if user.image != 'anony.png':
                    file = f'admin/image/{str(user.image)}'
                    remove_file(file)
                user.image = img

        db.session.commit()
        flash(f'Information Updated Successfully.', 'success')
        return redirect(url_for('.admin_settings'))

    form.name.data = user.name
    form.email.data = current_user.email
    form.phone.data = user.phone
    return render_template("admin/settings.html", title="Admin | Settings", form=form, user=user, admins=admins)

@admin.route("/admin/settings/add-admin/", methods=['GET', 'POST'])
@user_role_required('admin')
def admin_add():
    user = current_user.admins
    form = Admins_Add()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(email=form.email.data.lower(), user_role='admin', password=pw_hash)
        db.session.add(user)
        
        admin = Admin(name=form.name.data.strip().capitalize(), phone=form.phone.data, user=user)
        db.session.add(admin)
        db.session.commit()
        
        flash(f'New Admin Added Successfully!', 'success')
        return redirect(url_for('.admin_settings'))
    
    return render_template("admin/new.html", title="Admin | Settings", form=form, user=user)

@admin.route("/admin/<int:admin_id>/update-admin/", methods=['GET', 'POST'])
@user_role_required('admin')
def admin_update(admin_id):
    user = current_user.admins
    updated = Admin.query.get_or_404(admin_id)
    if updated.user == current_user:
        abort(403)
    form = Admins_Edit()
    form.id.data = int(admin_id)
    if form.validate_on_submit():
        updated.name = form.name.data.strip().capitalize()
        updated.user.email = form.email.data.lower()
        updated.phone = form.phone.data 

        db.session.commit()
        
        flash(f'Admin Updated Successfully!', 'success')
        return redirect(url_for('.admin_settings'))
        
    form.name.data = updated.name 
    form.email.data = updated.user.email
    form.phone.data = updated.phone 
    return render_template("admin/update.html", title="Admin | Settings", form=form, user=user, updated=updated)

@admin.route("/admin/<int:admin_id>/remove", methods=['POST'])
@user_role_required('admin')
def admin_remove(admin_id):
    user = Admin.query.get_or_404(admin_id)

    if user.user == current_user:
        abort(403)

    db.session.delete(user)
    db.session.delete(user.user)
    db.session.commit()

    if user.image and user.image != "anony.png":
        file = f'admin/image/{str(user.image)}'
        try:
            remove_file(file)
        except FileNotFoundError:
            flash(f'File not Found!', category='danger')

    flash(f'Admin Removed Successfully!', 'success')
    return redirect(url_for('.admin_settings'))

@admin.route("/admin/<int:admin_id>/delete-image", methods=['POST'])
@user_role_required('admin')
def delete_image(admin_id):
    user = Admin.query.get_or_404(admin_id)
    if not user.user == current_user:
        abort(403)

    if user.image and user.image != "anony.png":
        file = f'admin/image/{str(user.image)}'
        try:
            remove_file(file)
            user.image = 'anony.png'
            db.session.commit()
            flash(f'Image Removed Successfully!', category='success')
        except FileNotFoundError:
            user.image = 'anony.png'
            db.session.commit()
            flash(f'File not Found!', category='danger')
    
    return redirect(url_for('.admin_settings'))

@admin.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.admins:
        return redirect(url_for('.admin_account'))
    form = User_Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.admins and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Admin Login successs.', 'success')

            return redirect(request.args.get('next') or url_for('.admin_account'))
        else:
            flash(f'Invalid Email or Password! Please Try Again.', 'danger')
    return render_template("admin/login.html", title="OraJobs | Admin Login", form=form)

# Admin User password reset request
@admin.route("/admin/password-reset", methods=['GET', 'POST'])
def password_reset_request():
    if current_user.is_authenticated and current_user.admins:
        return redirect(url_for('.admin_account'))
    form = Forgot_Password()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            try:
                send_pwd_reset_email(user, 'admin', user.admins.name)
                flash('A password reset link has been sent to your email', 'info')
                return redirect(url_for('.admin_login'))
            except:
                flash('Something went wrong! Please Try Again.', 'warning')
                return redirect(url_for('.password_reset_request'))
        else:
            flash('Email not registered. Send the email you registered your account with.', 'warning')
            return redirect(url_for('.password_reset_request'))
    return render_template("forgot_password.html", title="Admin | Reset Password", form=form)

# Admin user password reset token
@admin.route("/admin/password-reset/<string:token>", methods=['GET', 'POST'])
def password_reset_link(token):
    if current_user.is_authenticated and current_user.admins:
        return redirect(url_for('.admin_account'))
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
        return redirect(url_for('.admin_login'))
    
    return render_template("reset_password.html", title="Admin | Reset Password", form=form)
