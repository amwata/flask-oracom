from flask import render_template, Blueprint,url_for, flash, redirect
from OraApp.forms import User_Login

admin = Blueprint('admin', __name__)

@admin.route("/admin")
@admin.route("/admin/dashboard")
def admin_dashboard():
    return "<h1>Admin dashboard<?h1>"


@admin.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    form = User_Login()
    if form.validate_on_submit():
        flash(f'Login Successful for {form.email.data}!', 'success')
        return redirect(url_for('main.home'))
        
    return render_template("admin/login.html", title="OraJobs | Admin Login", form=form)

