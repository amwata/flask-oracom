
from OraApp import db
from OraApp.models import Job
from flask import render_template, Blueprint, request, abort

jobs = Blueprint('jobs', __name__)


@jobs.route("/jobs/<int:job_id>/details/")
def profile(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template("jobs/profile.html", title="OraJobs | Job Details", job=job)

@jobs.route("/jobs/")
@jobs.route("/jobs/list/")
def job_list():
    page = request.args.get('page', 1, type=int)
    jobs = Job.query.order_by(Job.date_posted.desc()).paginate(page=page, per_page=15)

    query = db.session.query(Job.category.distinct().label('category'))
    filtered = Job.query
    categories = [row.category for row in query.all()]
    return render_template("jobs/list.html", title="OraJobs | Jobs List", jobs=jobs, filtered=filtered, categories=categories)

@jobs.route("/jobs/categories/")
def categories():
    page = request.args.get('page', 1, type=int)
    query = db.session.query(Job.category.distinct().label('category')).paginate(page=page, per_page=15)
    jobs = Job.query
    categories = [row.category for row in query.items]
    return render_template("jobs/categories.html", title="OraJobs | Jobs Categories", jobs=jobs, categories=categories,pages=query)


@jobs.route("/jobs/categories/<string:category>")
def filtered(category):
    page = request.args.get('page', 1, type=int)
    jobs = Job.query.filter_by(category=category).order_by(Job.date_posted.desc()).paginate(page=page, per_page=15) or abort(404)
    
    head = f'Jobs in {category}: {len(jobs.items)}'
    return render_template("jobs/filtered.html", title="OraJobs | Jobs List", jobs=jobs, head=head)