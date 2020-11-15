from flask import Blueprint

play = Blueprint('play', __name__, template_folder='templates', 
    static_folder='static', static_url_path='/app/play/static/'
)

from . import events, routes

