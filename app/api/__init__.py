from flask import Blueprint

api_bp = Blueprint('api', __name__)

from . import api

# def checkExistence(cid, term):


