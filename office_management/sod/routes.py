from flask import Blueprint
from office_management.sod.resources import UserSod


sod = Blueprint("sod", __name__)

sod.add_url_rule("/sod", view_func=UserSod.as_view("sod"))
