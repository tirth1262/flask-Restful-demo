from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from office_management.utils.decorators import admin_required
from office_management.sod import services


class UserSod(Resource):
    sod_services = services.SodServices(request)

    @jwt_required()
    def get(self):
        # return display_roles()
        return services.SodServices.display_sod()

    @classmethod
    @jwt_required()
    def post(cls):
        return cls.sod_services.add_sod()

    @classmethod
    @admin_required()
    def put(cls):
        return cls.sod_services.update_sod()

    @classmethod
    @jwt_required()
    def delete(cls):
        return cls.sod_services.delete_sod()
