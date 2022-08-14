from flask import Flask


def create_app():
    app = Flask(__name__)

    from OraApp.main.routes import main
    from OraApp.applicants.routes import applicant
    from OraApp.employers.routes import employer
    from OraApp.jobs.routes import jobs
    from OraApp.companies.routes import company
    from OraApp.admin.routes import admin
    from OraApp.errors.handlers import errors


    app.register_blueprint(main)
    app.register_blueprint(applicant)
    app.register_blueprint(employer)
    app.register_blueprint(company)
    app.register_blueprint(admin)
    app.register_blueprint(jobs)
    app.register_blueprint(errors)

    return app

