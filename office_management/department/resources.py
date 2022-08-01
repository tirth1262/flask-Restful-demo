from flask_restful import Resource
from office_management.utils.decorators import admin_required
from office_management.department.services import add_dept, all_dept, delete_dept, update_dept


class Department(Resource):
    @admin_required()
    def get(self):
        return all_dept()

    @admin_required()
    def post(self):
        return add_dept()

    @admin_required()
    def put(self):
        return update_dept()

    @admin_required()
    def delete(self):
        return delete_dept()
