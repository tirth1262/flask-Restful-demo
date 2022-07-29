from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from office_management.users.services import (login, register,
                                              user_profile,
                                              update_user_profile,
                                              update_official_profile,
                                              user_official_profile, update_personal_profile,
                                              user_personal_profile, update_password, delete_user, refresh)
from office_management.users.decorators import admin_required

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
    # @jwt_required()
    @admin_required()
    def get(self):
        return user_profile()

    @jwt_required()
    def put(self):
        return update_user_profile()

    @jwt_required()
    def delete(self):
        return delete_user()


class OfficialInformation(Resource):
    @jwt_required()
    def get(self):
        return user_official_profile()

    @jwt_required()
    def put(self):
        return update_official_profile()


class PersonalInfo(Resource):
    @jwt_required()
    def get(self):
        return user_personal_profile()

    @jwt_required()
    def put(self):
        return update_personal_profile()


class UpdatePassword(Resource):
    @jwt_required()
    def put(self):
        return update_password()