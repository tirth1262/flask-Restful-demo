from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from office_management.utils.decorators import admin_required
from office_management.sod import services


class UserSod(Resource):
    sod_services = services.SodServices(request)

    @jwt_required()
    def get(self, sod_id=None):
        return (services.SodServices.get_sod_by_id(sod_id) if sod_id
                else services.SodServices.get_all_sod())

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
