from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from os import path
from sqlalchemy import create_engine

dir = 'OraApp'
bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()
db_name = 'orajobs.db'

db_user = os.environ.get('DB_USER')
db_pwd = os.environ.get('DB_PWD')
secret_key = os.environ.get('SECRET_KEY')
xmp_soc = 'xampp mysql socket... ?unix_socket=/opt/lampp/var/mysql/mysql.sock'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    # sqlite db uri...app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_name}"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_pwd}@localhost/orajobs"
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



