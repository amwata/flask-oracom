
from OraApp.models import Job
from flask import render_template, Blueprint, request

jobs = Blueprint('jobs', __name__)


@jobs.route("/jobs/")
@jobs.route("/jobs/list")
def job_list():
    page = request.args.get('page', 1, type=int)
    jobs = Job.query.order_by(Job.date_posted.desc()).paginate(page=page, per_page=15)
    return render_template("jobs/list.html", title="OraJobs | Jobs List", jobs=jobs)

@jobs.route("/jobs/<int:job_id>/profile/")
def profile(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template("jobs/profile.html", title="OraJobs | Job Profile", job=job)
