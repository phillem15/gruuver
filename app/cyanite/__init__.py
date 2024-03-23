from flask import Blueprint, current_app
from . import views

cyanite = Blueprint('cyanite_integration', __name__)

# Configuration variables
SECRET = current_app.config['SECRET']
API_URL = current_app.config['API_URL']
ACCESS_TOKEN = current_app.config['ACCESS_TOKEN']
