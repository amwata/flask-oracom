from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, HiddenField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL
from flask_wtf.file import FileField, FileAllowed
from OraApp.models import User
from flask_login import current_user

# user login form
class User_Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = HiddenField(default='applicant')
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Admin(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    submit = SubmitField('Update Information')

    def validate_email(self, email):
        if email.data != current_user.email:
            exists = User.query.filter_by(email=email.data).first()  
            if exists:
                raise ValidationError('This email already in use!')

class Admin_Update(Admin):
    image = FileField('Image (jpg and png files)', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

class Admins_Add(Admin):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Add Admin')

    def validate_email(self, email):
        exists = User.query.filter_by(email=email.data).first()  
        if exists:
            raise ValidationError('This email is already registered!')

class Admins_Edit(Admin):
    id = HiddenField()
    submit = SubmitField('Update Admin')

    def validate_email(self, email):
        exists = User.query.filter_by(email=email.data).first()  
        if exists and exists.admins.id != int(self.id.data):
            raise ValidationError(f'Email ({email.data}) already in use!')

# Applicant data form
class Applicant(FlaskForm):
    f_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    l_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    resume = FileField('Resume (pdf and doc files)', validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx'])])
    image = FileField('Optional Photo (jpg and png files)', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    role = HiddenField(default='applicant')
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        exists = User.query.filter_by(email=email.data).first()  
        if exists:
            raise ValidationError('This email is Taken! Sign in instead.') 

class Applicant_Signup(Applicant):
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) 

class Applicant_Add(Applicant):
    submit = SubmitField('Add Account')

    def validate_email(self, email):
        exists = User.query.filter_by(email=email.data).first()  
        if exists:
            raise ValidationError('This email is Taken!') 

class Applicant_Update(Applicant):
    id = HiddenField()
    resume = FileField('Resume (pdf and doc files)', validators=[FileAllowed(['pdf', 'doc', 'docx'])])
    password = None
    submit = SubmitField('Update Account')

    def validate_email(self, email):
        exists = User.query.filter_by(email=email.data).first()  
        if exists and exists.applicants.id != int(self.id.data):
            raise ValidationError(f'Email ({email.data}) already in use!')

class Applicant_User_Update(Applicant):
    resume = FileField('Resume (pdf and doc files)', validators=[FileAllowed(['pdf', 'doc', 'docx'])])
    password = None
    submit = SubmitField('Update Account')

    def validate_email(self, email):
        if email.data != current_user.email:
            exists = User.query.filter_by(email=email.data).first()  
            if exists:
                raise ValidationError('This email already in use!')

# Employer Registration form
class Employer_Signup(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=60)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    location = StringField('Location', validators=[DataRequired()])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    tagline = StringField('Tagline (Advertising Slogan)', validators=[DataRequired(), Length(min=5, max=120)])
    description = TextAreaField('Company Description', validators=[DataRequired(), Length(min=5, max=1000)])
    website = StringField('Company Website (Optional)')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    logo = FileField('Logo (jpg and png files)', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    role = HiddenField(default='employer')
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        exists = User.query.filter_by(email=email.data).first()  
        if exists:
            raise ValidationError('This email is Taken! Sign in instead.')

class Employer_Add(Employer_Signup):
    submit = SubmitField('Add Account')

    def validate_email(self, email):
        exists = User.query.filter_by(email=email.data).first()  
        if exists:
            raise ValidationError('This email is Taken!') 

class Employer_Update(Employer_Signup):
    id = HiddenField()
    password = None
    submit = SubmitField('Update Account')

    def validate_email(self, email):
        exists = User.query.filter_by(email=email.data).first()  
        if exists and exists.employers.id != int(self.id.data):
            raise ValidationError(f'Email ({email.data}) already in use!')

class Employer_User_Update(Employer_Signup):
    password = None
    submit = SubmitField('Update Account')

    def validate_email(self, email):
        if email.data != current_user.email:
            exists = User.query.filter_by(email=email.data).first()  
            if exists:
                raise ValidationError('This email already in use!')

class Job_Add(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired(), Length(min=2, max=100)])
    category = StringField('Job Category', validators=[DataRequired(), Length(min=2, max=100)])
    type = SelectField('Job Type', validators=[DataRequired(), Length(min=2, max=20)], choices=['Long-Term', 'Short-Term', 'Full Time', 'Part Time', 'Contract', 'Internship'])
    description = TextAreaField('Job Description', validators=[DataRequired(), Length(min=5, max=1000)])
    salary = StringField('Salary (Optional) KSh.')
    company_id = IntegerField('Company ID', validators=[DataRequired()])
    submit = SubmitField('Post Job')

    def validate_salary(self, salary):
        if salary.data != '':
            try:
                float(salary.data)
            except ValueError:
                raise ValidationError(f'Invalid Salary value!')

class Job_Update(Job_Add):
    company_id = None
    submit = SubmitField('Update Job')

# Job Search form
class Job_Search(FlaskForm):
    title = StringField('Job Title/Category', validators=[DataRequired(), Length(min=2, max=100)])
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Search')

# Company search form
class Company_Search(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Search')

class Forgot_Password(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Email')
    def validate_email(self, email):
        exists = User.query.filter_by(email=email.data).first()  
        if not exists:
            raise ValidationError('Email Not Registered! Use your account\'s verified Email.') 


class Reset_Password(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) 
    submit = SubmitField('Reset Password')


     
