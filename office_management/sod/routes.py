from flask import Blueprint
from flask_restful import Api

from office_management.sod.resources import UserSod


sod = Blueprint("sod", __name__)

sod.add_url_rule("/sod", view_func=UserSod.as_view("sod"))
sod_rest_api = Api(sod)

# roles.add_url_rule("/roles/<int:role_id>", view_func=UserRoles.as_view("roles"))
# roles.add_url_rule("/roles", view_func=UserRoles.as_view("roles"))

sod_rest_api.add_resource(UserSod, '/sod', '/sod/<int:sod_id>')