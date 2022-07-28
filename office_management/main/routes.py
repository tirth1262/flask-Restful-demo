from flask import Blueprint
from office_management.main.resources import Hello

main = Blueprint("main", __name__)

main.add_url_rule("/hello/<int:userid>", view_func=Hello.as_view("hello"))