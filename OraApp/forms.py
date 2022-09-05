from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL
from flask_wtf.file import FileField, FileAllowed
from OraApp.models import User


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
    resume = FileField('Resume (pdf and doc files)', validators=[DataRequired(), FileAllowed(['pdf', 'doc'])])
    image = FileField('Optional Photo (jpg and png files)', validators=[FileAllowed(['jpg', 'png'])])
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
    logo = FileField('Logo (jpg and png files)', validators=[FileAllowed(['jpg', 'png'])])
    role = HiddenField(default='employer')
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        exists = User.query.filter_by(email=email.data).first()  
        if exists:
            raise ValidationError('This email is Taken! Sign in instead.')

class Admin_Info_Update(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8)])
    image = FileField('Image (jpg and png files)', validators=[FileAllowed(['jpg', 'png'])])
    role = HiddenField(default='admin')
    submit = SubmitField('Update Information')

    def validate_email(self, email):
        exists = User.query.filter_by(email=email.data).first()  
        if exists:
            raise ValidationError('This email is Taken! Sign in instead.')

class Job_Search(FlaskForm):
    pass

class Contact_Form(FlaskForm):
    pass

class Reset_Password(FlaskForm):
    pass
