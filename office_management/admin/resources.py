from flask_jwt_extended import jwt_required
from flask_restful import Resource
from office_management.admin.services import all_roles, add_role, delete_role, update_role
from office_management.users.decorators import admin_required


class UserRoles(Resource):
    @jwt_required()
    def get(self):
        return all_roles()

    @admin_required()
    def post(self):
        return add_role()

    @admin_required()
    def put(self):
        return update_role()

    @admin_required()
    def delete(self):
        return delete_role()
