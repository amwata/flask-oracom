import secrets, os
from flask import current_app, url_for, redirect, flash, request
from PIL import Image
from flask_login import current_user
from functools import wraps
from OraApp.models import User


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

def remove_file(file):
    file_path = os.path.join(current_app.root_path, f'static/{file}')
    os.remove(file_path)


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
    