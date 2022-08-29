from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from os import path
from sqlalchemy import create_engine

dir = 'OraApp'
bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()
db_name = 'orajobs.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "7739bb95607822a2c3a07f6ad3d02dd"
    # sqlite db uri...app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_name}"
    #xampp mysql socket... ?unix_socket=/opt/lampp/var/mysql/mysql.sock
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:#nother0NE@localhost/orajobs"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)


    from .main.routes import main
    from .applicants.routes import applicant
    from .employers.routes import employer
    from .jobs.routes import jobs
    from .admin.routes import admin
    from .errors.handlers import errors


    app.register_blueprint(main)
    app.register_blueprint(applicant)
    app.register_blueprint(employer)
    app.register_blueprint(admin)
    app.register_blueprint(jobs)
    app.register_blueprint(errors)

    # db.create_all(app=app)
    # create_db(app)

    return app

# creating sqlite database in app directory
# def create_db(app):
#     if not path.exists(f'{dir}/{db_name}'):
#         db.create_all(app=app)



