from flask_jwt_extended import jwt_required
from flask_restful import Resource, fields, marshal_with

from office_management.users.models import User


class AllCapsString(fields.Raw):
    def format(self, value):
        return value.title()


resource_fields = {
    'username': fields.String(default='Anonymous User'),
    'email': AllCapsString(attribute='email'),
}


class Hello(Resource):
    @marshal_with(resource_fields)
    @jwt_required()
    def get(self, userid):
        new = User.query.filter_by(id=userid).first()
        return new
