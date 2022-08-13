from flask import Flask

app = Flask(__name__)

from app.admin import routes
from app.applicants import routes
from app.employers import routes
from app.jobs import routes
from app.main import routes
from app.companies import routes
