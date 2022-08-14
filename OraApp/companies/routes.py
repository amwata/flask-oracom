from flask import render_template, Blueprint

company = Blueprint('company', __name__)

@company.route("/companies")
def company_list():
    return render_template("companies/list.html", title="OraJobs | Jobs List")