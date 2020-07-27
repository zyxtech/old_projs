from flask import Blueprint

demos = Blueprint('demos', __name__)

from . import views
