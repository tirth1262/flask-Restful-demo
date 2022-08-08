from flask import Blueprint
from office_management.leaves.resources import LeaveRequest, LeaveComments,Holidays, Leaves


leaves = Blueprint("leaves", __name__)

leaves.add_url_rule("/leaves", view_func=LeaveRequest.as_view("leaves"))
leaves.add_url_rule("/leaves/comments/", view_func=LeaveComments.as_view("comments"))
leaves.add_url_rule("/leaves/holidays", view_func=Holidays.as_view("holidays"))
leaves.add_url_rule("/leaves/my", view_func=Leaves.as_view("my_leaves"))



