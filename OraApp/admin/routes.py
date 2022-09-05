
from flask import render_template, Blueprint, url_for, flash, redirect, request, abort
from OraApp import db, bcrypt
from OraApp.forms import User_Login, Admin_Info_Update
from OraApp.models import Admin, User
from OraApp.utils import user_role_required, remove_file
from flask_login import login_user, current_user


admin = Blueprint('admin', __name__)

# @admin.route("/admin")
@admin.route("/admin/dashboard/")
@user_role_required('admin')
def admin_account():
    user = Admin.query.filter_by(user_id=current_user.id).first()
    return render_template("admin/dashboard.html", title="Admin | Dashboard", user=user )

@admin.route("/admin/job-categores/")
@user_role_required('admin')
def admin_job_categories():
    user = Admin.query.filter_by(user_id=current_user.id).first()
    return render_template("admin/dashboard.html", title="Admin | Job Categories")

@admin.route("/admin/companies/")
@user_role_required('admin')
def admin_companies():
    user = Admin.query.filter_by(user_id=current_user.id).first()
    return render_template("admin/dashboard.html", title="Admin | Manage Companies")

@admin.route("/admin/applicants/")
@user_role_required('admin')
def admin_applicants():
    user = Admin.query.filter_by(user_id=current_user.id).first()
    return render_template("admin/dashboard.html", title="Admin | Manage Applicants")

@admin.route("/admin/notifications/")
@user_role_required('admin')
def admin_notifications():
    user = Admin.query.filter_by(user_id=current_user.id).first()
    return render_template("admin/dashboard.html", title="Admin | Notifications")

@admin.route("/admin/settings/", methods=['GET', 'POST'])
@user_role_required('admin')
def admin_settings():
    user = Admin.query.filter_by(user_id=current_user.id).first()
    admins = Admin.query.all()
    form = Admin_Info_Update()
    form.name.data = user.name
    form.email.data = current_user.email
    form.phone.data = user.phone
    return render_template("admin/settings.html", title="Admin | Settings", form=form, user=user, admins=admins)

@admin.route("/admin/<int:admin_id>/delete-image", methods=['POST'])
@user_role_required('admin')
def delete_image(admin_id):
    user = Admin.query.get_or_404(admin_id)
    if not user.admin == current_user:
        abort(403)

    if user.image and user.image != "anony.png":
        file = f'admin/image/{str(user.image)}'

    try:
        remove_file(file)
        user.image = 'anony.png'
        db.session.commit()
        flash(f'Image Removed Successfully!', category='success')
    except FileNotFoundError:
        flash(f'File not Found!', category='danger')
    
    return redirect(url_for('.admin_settings'))


@admin.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.user_role == 'admin':
        return redirect(url_for('.admin_account'))
    form = User_Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.user_role == 'admin' and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Admin Login successs.', 'success')

            return redirect(request.args.get('next') or url_for('.admin_account'))
        else:
            flash(f'Invalid Email or Password! Please Try Again.', 'danger')
    return render_template("admin/login.html", title="OraJobs | Admin Login", form=form)