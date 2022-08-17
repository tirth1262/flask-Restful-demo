from flask import request
from flask_restful import Resource

from office_management.department import services
from office_management.utils.decorators import admin_required


class Department(Resource):
    department_services = services.DeptServices(request)

    @admin_required()
    def get(self, dept_id=None):
        return (services.DeptServices.get_dept_by_id(dept_id) if dept_id
                else services.DeptServices.get_all_department())

    @classmethod
    @admin_required()
    def post(cls):
        return cls.department_services.add_dept()

    @classmethod
    @admin_required()
    def put(cls):
        return cls.department_services.update_dept()

    @classmethod
    @admin_required()
    def delete(cls):
        return cls.department_services.delete_dept()
