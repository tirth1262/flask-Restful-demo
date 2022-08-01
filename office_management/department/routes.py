from flask import Blueprint
from office_management.department.resources import Department

departments = Blueprint("departments", __name__)

departments.add_url_rule("/departments", view_func=Department.as_view("departments"))