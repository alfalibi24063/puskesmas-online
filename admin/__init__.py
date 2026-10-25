from flask import Blueprint


radmin = Blueprint("radmin",__name__)
from admin import routes
