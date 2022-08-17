from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from office_management.utils.decorators import admin_required
from office_management.eod import services


class UserEod(Resource):
    eod_services = services.EodServices(request)

    @jwt_required()
    def get(self, eod_id=None):
        return (services.EodServices.get_eod_by_id(eod_id) if eod_id
                else services.EodServices.get_all_eod())

    @classmethod
    @jwt_required()
    def post(cls):
        return cls.eod_services.add_eod()

    @classmethod
    @jwt_required()
    def put(cls):
        return cls.eod_services.update_eod()

    @classmethod
    @jwt_required()
    def delete(cls):
        return cls.eod_services.delete_eod()
