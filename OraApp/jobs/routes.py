
from OraApp import db
from OraApp.models import Job, jobs_applied, Employer
from flask import render_template, Blueprint, request, abort
from OraApp.forms import Job_Search

jobs = Blueprint('jobs', __name__)

# Job details
@jobs.route("/jobs/<int:job_id>/details/")
def profile(job_id):
    job = Job.query.get_or_404(job_id)
    query = db.session.query(jobs_applied.c.shortlisted).filter_by(job_id=job_id)
    return render_template("jobs/profile.html", title="OraJobs | Job Details", job=job, query=query)

# List of all jobs
@jobs.route("/jobs/")
@jobs.route("/jobs/list/")
def job_list():
    form1 = Job_Search()
    page = request.args.get('page', 1, type=int)
    jobs = Job.query.order_by(Job.date_posted.desc()).paginate(page=page, per_page=15)

    query = db.session.query(Job.category.distinct().label('category'))
    filtered = Job.query
    categories = [row.category for row in query.all()]
    return render_template("jobs/list.html", title="OraJobs | Jobs List", jobs=jobs, filtered=filtered, form1=form1, categories=categories)

@jobs.route("/jobs/categories/")
def categories():
    form1 = Job_Search()
    page = request.args.get('page', 1, type=int)
    query = db.session.query(Job.category.distinct().label('category')).paginate(page=page, per_page=15)
    jobs = Job.query
    categories = [row.category for row in query.items]
    return render_template("jobs/categories.html", title="OraJobs | Jobs Categories", jobs=jobs, form1=form1, categories=categories,pages=query)

# Filter jobs by category
@jobs.route("/jobs/categories/<string:category>")
def filtered(category):
    form1 = Job_Search()
    page = request.args.get('page', 1, type=int)
    jobs = Job.query.filter_by(category=category).order_by(Job.date_posted.desc()).paginate(page=page, per_page=15) or abort(404)
    
    head = f'{category} Jobs'
    return render_template("jobs/filtered.html", title="OraJobs | Jobs List", jobs=jobs, form1=form1, head=head)

# Jobs search
@jobs.route("/jobs/search", methods=['POST'])
def job_search():
    form1 = Job_Search()
    form = request.form
    title_or_category = form['title']
    location = form['location']
    search1 = "%{0}%".format(title_or_category)
    search2 = "%{0}%".format(location)

    page = request.args.get('page', 1, type=int)

    jobs = db.session.query(Job).select_from(Job).filter((Job.title.like(search1) | Job.category.like(search1))).join(Employer).filter(Employer.location.like(search2)).order_by(Job.date_posted.desc()).paginate(page=page, per_page=15) 

    
    locations = f'in "{ location }"' if location else ''
    head = f'Search Results for "{ title_or_category }" {locations}'
    return render_template("jobs/filtered.html", title="OraJobs | Job Search", jobs=jobs, head=head, form1=form1)