from flask import Blueprint
from flask_restful import Api

from office_management.eod.resources import UserEod


eod = Blueprint("eod", __name__)
eod_rest_api = Api(eod)

eod_rest_api.add_resource(UserEod, '/eod', '/eod/<int:eod_id>')
