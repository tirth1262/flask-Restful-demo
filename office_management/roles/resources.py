from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from office_management.utils.decorators import admin_required
from office_management.roles import services


class UserRoles(Resource):
    role_services = services.RoleServices(request)

    @jwt_required()
    def get(self, role_id=None):
        return (services.RoleServices.get_role_by_id(role_id) if role_id
                else services.RoleServices.get_all_roles())


    @classmethod
    @admin_required()
    def post(cls):
        return cls.role_services.create_role()

    @classmethod
    @admin_required()
    def put(cls):
        return cls.role_services.update_role()

    @classmethod
    @admin_required()
    def delete(cls):
        return cls.role_services.delete_role()
