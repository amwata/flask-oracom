from flask import render_template
from app import app

@app.route("/companies")
def companies():
    return render_template("jobs.html", title="OraJobs | Jobs List")