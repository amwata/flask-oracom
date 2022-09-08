from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL
from flask_wtf.file import FileField, FileAllowed
from OraApp.models import User
from flask_login import current_user


class User_Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = HiddenField(default='applicant')
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Applicant_Signup(FlaskForm):
    f_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    l_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) 
    resume = FileField('Resume (pdf and doc files)', validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx'])])
    image = FileField('Optional Photo (jpg and png files)', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    role = HiddenField(default='applicant')
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        exists = User.query.filter_by(email=email.data).first()  
        if exists:
            raise ValidationError('This email is Taken! Sign in instead.') 





class Employer_Signup(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=20)])
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








class Admin_Update(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    image = FileField('Image (jpg and png files)', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update Information')

    def validate_email(self, email):
        if email.data != current_user.email:
            exists = User.query.filter_by(email=email.data).first()  
            if exists:
                raise ValidationError('This email already in use!')

class Admin_Add(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Add Admin')

    def validate_email(self, email):
        exists = User.query.filter_by(email=email.data).first()  
        if exists:
            raise ValidationError('This email is already registered!')

class Admin_Edit(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    id = HiddenField()
    submit = SubmitField('Update Admin')

    def validate_email(self, email):
        exists = User.query.filter_by(email=email.data).first()  
        if exists and exists.admins[0].id != int(self.id.data):
            raise ValidationError(f'Email ({email.data}) already in use!')

class Admin_Applicant_Add(FlaskForm):
    f_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    l_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    resume = FileField('Resume (pdf and doc files)', validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx'])])
    submit = SubmitField('Add')

    def validate_email(self, email):
        exists = User.query.filter_by(email=email.data).first()  
        if exists:
            raise ValidationError('This email is Taken!') 

class Admin_Applicant_Update(FlaskForm):
    f_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    l_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    resume = FileField('Resume (pdf and doc files)', validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx'])])
    id = HiddenField()
    submit = SubmitField('Update')

    def validate_email(self, email):
        exists = User.query.filter_by(email=email.data).first()  
        if exists and exists.applicants[0].id != int(self.id.data):
            raise ValidationError(f'Email ({email.data}) already in use!')



class Job_Search(FlaskForm):
    pass

class Contact_Form(FlaskForm):
    pass

class Reset_Password(FlaskForm):
    pass
