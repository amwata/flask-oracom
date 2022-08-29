
from flask import render_template, Blueprint, url_for, flash, redirect, request
from OraApp import bcrypt
from OraApp.forms import User_Login
from OraApp.models import Admin, User
from OraApp.utils import user_role_required
from flask_login import login_user, current_user


admin = Blueprint('admin', __name__)

@admin.route("/admin")
@admin.route("/admin/dashboard")
@user_role_required('admin')
def admin_dashboard():
    user = Admin.query.filter_by(user_id=current_user.id).first()
    return render_template("admin/dashboard.html", title="OraJobs | Admin Dashboard", email=user.name)



@admin.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.user_role == 'admin':
        return redirect(url_for('.admin_dashboard'))
    form = User_Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.user_role == 'admin' and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Login successs.', 'info')

            return redirect(request.args.get('next') or url_for('.admin_dashboard'))
        else:
            flash(f'Invalid Email or Password! Please Try Again.', 'danger')
    return render_template("admin/login.html", title="OraJobs | Admin Login", form=form)