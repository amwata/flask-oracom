import secrets, os
from flask import current_app, url_for, redirect, flash, request, render_template
from PIL import Image
from flask_login import current_user
from functools import wraps
from OraApp import mail
from flask_mail import Message

# function to save file documents
def save_file(dir, file):
    rand_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(file.filename)
    file_name = rand_hex + file_ext
    file_path = os.path.join(current_app.root_path, f'static/{dir}', file_name)

    try:
        if file_ext == '.jpg' or file_ext == '.png':
            img_size = (125, 125)
            img = Image.open(file)
            img.thumbnail(img_size)
            img.save(file_path)
        else:
            file.save(file_path)
    except FileNotFoundError:
        flash(message='Inappropriate File or Directory!', category='danger')
    return file_name

# Delete saved files
def remove_file(file):
    file_path = os.path.join(current_app.root_path, f'static/{file}')
    os.remove(file_path)

# Authorize authenticated users
def user_role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.user_role != role:
                url = request.url
                flash(f'{role.capitalize()} Login Required for this Page!', category='info')
                return redirect(url_for(f'{role.lower()}.{role.lower()}_login', next= url))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

#  sending email for reseting a user's password
def send_pwd_reset_email(user, role, name):
    token = user.get_reset_token() 

    subject = 'Password Reset'
    sender = ('OraJobs', 'saseda0@gmail.com')
    recipients = [user.email]

    link = url_for(f'{role}.password_reset_link', token=token, _external=True)
    resend = url_for(f'{role}.password_reset_request', _external=True)
    img = url_for('static', filename='img/oj.png', _external=True)

    html = render_template('email.html', link=link, name=name, img=img, resend=resend)
    msg = Message(subject=subject, sender=sender, recipients=recipients, html=html)
    mail.send(msg)

#  sending email to shortlisted applicants
def send_shortlist_email(email, obj):

    subject = 'You are Shortlisted'
    sender = ('OraJobs', 'saseda0@gmail.com')
    recipients = [email]

    jobs = url_for('jobs.job_list', _external=True)
    # img = url_for('static', filename='img/oj.png', _external=True)

    html = render_template('email.html', shortlist=obj, jobs=jobs)
    msg = Message(subject=subject, sender=sender, recipients=recipients, html=html)
    mail.send(msg)
