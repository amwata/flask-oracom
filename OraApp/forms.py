from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FileField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from OraApp.models import Applicant


class User_Login(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                        validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Applicant_Signup(FlaskForm):
    f_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    l_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) 
    resume = FileField('Resume(pdf and doc files only)', validators=[DataRequired()])
    image = FileField('Photo')
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        exists = Applicant.query.filter_by(email=email.data).first()  
        if exists:
            raise ValidationError('This email is Taken! Sign in instead.') 


class Employer_Signup(FlaskForm):
    concern_name = StringField('Concern Person Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone = IntegerField('Phone Number',
                            validators=[DataRequired()])
    tagline = StringField('Tagline (Advertising Slogan)',
                        validators=[DataRequired(), Length(min=5, max=120)])
    description = StringField('Description',
                        validators=[DataRequired(), Length(min=5, max=1000)])
    web_url = StringField('Website', validators=[Length(min=2, max=120)])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')]) 
    logo = FileField('Logo', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class Job_Search(FlaskForm):
    pass

class Contact_Form(FlaskForm):
    pass

class Reset_Password(FlaskForm):
    pass