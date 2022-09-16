
from OraApp.models import Job
from flask import render_template, Blueprint

jobs = Blueprint('jobs', __name__)


@jobs.route("/jobs")
def job_list():
    jobs = Job.query.all()
    return render_template("jobs/list.html", title="OraJobs | Jobs List", jobs=jobs)

