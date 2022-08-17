from flask import Blueprint
from flask_restful import Api
from office_management.roles.resources import UserRoles

roles = Blueprint("roles", __name__)
role_rest_api = Api(roles)

# roles.add_url_rule("/roles/<int:role_id>", view_func=UserRoles.as_view("roles"))
# roles.add_url_rule("/roles", view_func=UserRoles.as_view("roles"))

role_rest_api.add_resource(UserRoles, '/roles', '/roles/<int:role_id>')
