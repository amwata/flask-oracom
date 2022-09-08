from datetime import datetime
from OraApp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_role = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    applicants = db.relationship('Applicant', backref='applicant', lazy=True)
    admins = db.relationship('Admin', backref='admin', lazy=True)
    employers = db.relationship('Employer', backref='employer', lazy=True)

class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(20), nullable=False)
    l_name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    resume = db.Column(db.String(25), nullable=False)
    image = db.Column(db.String(25),  nullable=False, default='anony.png')
    date_joined = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Employer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(20), nullable=False)
    tagline = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    website = db.Column(db.String(20))
    logo = db.Column(db.String(25),  nullable=False, default='company.png')
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(20),  nullable=False, default='anony.png')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(20), nullable=False)
    salary = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(20), nullable=False)
    # category = db.Column(db.String(20), nullable=False)
    # sender = db.Column(db.String(20), nullable=False)
    # receipient = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)