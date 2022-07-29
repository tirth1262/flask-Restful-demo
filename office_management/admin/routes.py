from flask import Blueprint
from office_management.admin.resources import UserRoles

administer = Blueprint("administer", __name__)

administer.add_url_rule("/roles", view_func=UserRoles.as_view("roles"))
