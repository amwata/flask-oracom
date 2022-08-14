from flask import render_template, Blueprint

admin = Blueprint('admin', __name__)

@admin.route("/admin")
@admin.route("/admin/dashboard")
def admin_dashboard():
    return "<h1>Admin dashboard<?h1>"


@admin.route("/admin/login")
def admin_login():
    return render_template("admin/login.html", title="OraJobs | Admin Login")

