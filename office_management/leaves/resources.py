from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from office_management.leaves import services
from office_management.leaves.services import leave_request, display_comments, leave_comment, display_user_leaves
from office_management.utils.decorators import admin_required


class Leaves(Resource):
    @jwt_required()
    def get(self):
        return display_user_leaves()


class LeaveRequest(Resource):
    @jwt_required()
    def post(self):
        return leave_request()


class LeaveComments(Resource):
    @jwt_required()
    def get(self):
        return display_comments()

    @jwt_required()
    def post(self):
        return leave_comment()


class Holidays(Resource):
    holidays_services = services.HolidayServices(request)

    @admin_required()
    def get(self):
        return services.HolidayServices.display_holidays()

    @classmethod
    @admin_required()
    def post(cls):
        return cls.holidays_services.add_holiday()

    @admin_required()
    def put(self):
        return services.HolidayServices.update_holiday()

    @classmethod
    @admin_required()
    def delete(cls):
        return cls.holidays_services.delete_holiday()
