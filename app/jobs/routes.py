from flask import render_template
from app import app


@app.route("/jobs")
def jobs():
    return render_template("jobs.html", title="OraJobs | Jobs List")
