from flask import render_template, Blueprint

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(403)
def error_403(error):
    return render_template("errors/403.html", title="OraJobs | Error: 403"), 403

@errors.app_errorhandler(404)
def error_404(error):
    return render_template("errors/404.html", title="OraJobs | Error: 404"), 404

@errors.app_errorhandler(405)
def error_405(error):
    return render_template("errors/405.html", title="OraJobs | Error: 405"), 405

@errors.app_errorhandler(500)
def error_500(error):
    return render_template("errors/500.html", title="OraJobs | Error: 500"), 500


