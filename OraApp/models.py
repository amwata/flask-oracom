
from flask import current_app
from datetime import datetime
from OraApp import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_role = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    applicants = db.relationship('Applicant', backref='user', uselist=False, lazy=True)
    admins = db.relationship('Admin', backref='user', uselist=False, lazy=True)
    employers = db.relationship('Employer', backref='user', uselist=False, lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

# Association Table for connecting applicants to jobs table using a many-to-many relationship
jobs_applied = db.Table(
    'jobs_applied',
    db.Column('job_id',db.Integer, db.ForeignKey('jobs.id'), nullable=False),
    db.Column('applicant_id',db.Integer, db.ForeignKey('applicants.id'), nullable=False),
    db.Column('date_applied', db.DateTime(timezone=True), nullable=False, default=datetime.utcnow),
    db.Column('shortlisted', db.Boolean, nullable=False, server_default='0'),
    db.PrimaryKeyConstraint('job_id', 'applicant_id')
)

class Applicant(db.Model):
    __tablename__ = 'applicants'
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(20), nullable=False)
    l_name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    resume = db.Column(db.String(25), nullable=False)
    image = db.Column(db.String(25),  nullable=False, default='anony.png')
    applied_jobs = db.relationship('Job', secondary=jobs_applied, backref='applicants', lazy=True)
    date_joined = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

class Employer(db.Model):
    __tablename__ = 'employers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(20), nullable=False)
    tagline = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=False)
    website = db.Column(db.String(60))
    logo = db.Column(db.String(25),  nullable=False, server_default='company.png')
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    jobs = db.relationship('Job', backref='company', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(20),  nullable=False, server_default='anony.png')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(60), nullable=False)
    salary = db.Column(db.Float(20), nullable=False, server_default='0')
    type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey('employers.id'), nullable=False)

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(20), nullable=False)
    # category = db.Column(db.String(20), nullable=False)
    # sender = db.Column(db.String(20), nullable=False)
    # receipient = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)