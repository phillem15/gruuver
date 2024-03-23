from flask import Blueprint

cyanite = Blueprint('cyanite', __name__, template_folder='templates', static_folder='static')

from . import views
