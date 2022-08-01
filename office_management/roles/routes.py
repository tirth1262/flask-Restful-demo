from flask import Blueprint
from office_management.roles.resources import UserRoles

roles = Blueprint("roles", __name__)

roles.add_url_rule("/roles", view_func=UserRoles.as_view("roles"))
