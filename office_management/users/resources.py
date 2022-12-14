from flask_restful import Resource
from flask_jwt_extended import jwt_required
from office_management.users.services import (login, register,
                                              user_detail,
                                              update_user_detail,
                                              update_password, delete_user, refresh, display_heads)
from office_management.utils.decorators import admin_required


class Login(Resource):
    def post(self):
        return login()


class RefreshToken(Resource):
    @jwt_required()
    def post(self):
        return refresh()


class Register(Resource):
    @jwt_required()
    def post(self):
        return register()


class Profile(Resource):
    @jwt_required()
    def get(self):
        return user_detail()

    @jwt_required()
    def put(self):
        return update_user_detail()

    @admin_required()
    def delete(self):
        return delete_user()


class UpdatePassword(Resource):
    @jwt_required()
    def put(self):
        return update_password()


class UserHead(Resource):
    @jwt_required()
    def get(self):
        return display_heads()