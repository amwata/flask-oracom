from datetime import datetime
from OraApp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_applicant(id):
    return Applicant.query.get(int(id))

class Applicant(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(20), nullable=False)
    l_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    resume = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(20),  nullable=False, default='anony.png')
    password = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f"Applicant('{self.f_name}', '{self.l_name}', '{self.email}')"


class Employer():
    pass

class Admin():
    pass

class Job():
    pass

class Company():
    pass