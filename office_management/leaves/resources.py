from flask_restful import Resource
from flask_jwt_extended import jwt_required
from office_management.leaves.services import leave_request, display_comments, leave_comment, display_holidays, \
    update_holiday, add_holiday, delete_holiday, display_user_leaves
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
    @admin_required()
    def get(self):
        return display_holidays()

    @admin_required()
    def post(self):
        return add_holiday()

    @admin_required()
    def put(self):
        return update_holiday()

    @admin_required()
    def put(self):
        return delete_holiday()
