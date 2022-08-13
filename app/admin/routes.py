from flask import render_template
from app import app

@app.route("/admin")
@app.route("/admin/dashboard")
def adminHome():
    return "<h1>Admin dashboard<?h1>"


@app.route("/admin/login")
def adminLogin():
    return render_template("admin-login.html", title="OraJobs | Admin Login")

