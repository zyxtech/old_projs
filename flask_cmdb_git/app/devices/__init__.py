from flask import Blueprint

devices = Blueprint('devices', __name__ , template_folder='devices')

from . import views
from . import listviews
