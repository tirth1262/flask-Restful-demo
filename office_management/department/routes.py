from flask import Blueprint
from flask_restful import Api
from office_management.department.resources import Department

departments = Blueprint("departments", __name__)
department_rest_api = Api(departments)
department_rest_api.add_resource(Department, '/departments', '/departments/<int:dept_id>')

