from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, current_user, create_refresh_token
from marshmallow import ValidationError
from office_management import db, bcrypt, jwt
from office_management.users.models import User, UserRole
from office_management.users.schemas import (UserSchema, RegisterSchema,
                                             UserProfileSchema, UpdatePasswordSchema)
from office_management.users.validators import user_validation


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
        :param _jwt_header:
        :param jwt_data:
        :return: IT'S GET CURRENT USER ID AND FETCH USER FROM TABLE AND RETURN A USER OBJECT
    """
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


def login():
    login_schema = UserSchema()
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    try:
        data = login_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422
    email = data["email"]
    password = data["password"]
    user = User.query.filter_by(email=email).first()
    if user:
        if email != user.email or not bcrypt.check_password_hash(user.password, password):
            return jsonify({"msg": "Bad username or password"}), 401
    else:
        return jsonify({"msg": "User not Found."})
    access_token = create_access_token(identity=user.id,
                                       additional_claims={"role": f'{user.user_role[0].role_id}'})
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


def refresh():
    """
        This function is for create a new
        access token using current user id called refresh token,
        It's used to create refresh token
            :return: NEW ACCESS TOKEN
    """
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


def register():
    user_role = user_validation(get_jwt_identity())
    if user_role == 1:
        register_schema = RegisterSchema()
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        # Validate and deserialize input
        try:
            hs_pw = bcrypt.generate_password_hash(json_data['password']).decode('utf-8')
            json_data['password'] = hs_pw
            data = register_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        db.session.add(data)
        db.session.commit()
        new_role = UserRole(user_id=data.id, role_id=json_data["role_id"])

        db.session.add(new_role)
        db.session.commit()
        return {"message": f"{data.username} named new user created Successfully."}, 200
    else:
        return {"message": "You don't have Credential to perform this action."}, 401


# THIS FUNCTION GET CURRENT USER DATA FROM USER TABLE
def user_detail():
    user = User.query.filter_by(id=get_jwt_identity()).first()
    if user:
        user_detail_schema = UserProfileSchema()
        result = user_detail_schema.dump(user)
        return {"User": result}
    else:
        return {"message": "User no found!."}, 401


def update_user_detail():
    """
    THIS FUNCTION IS UPDATE "firstname" and "lastname" FROM "User".
    """
    user_id = get_jwt_identity()
    profile_of_user = User.query.filter_by(id=user_id).first()
    if profile_of_user:
        # Take only firstname and lastname from json data due to only
        user_profile_schema = UserProfileSchema(only=("firstname", "lastname"))
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        # Validate and deserialize input
        try:
            # Due to "instance" pass in load auto object add in user Model
            data = user_profile_schema.load(json_data, instance=profile_of_user)
            db.session.commit()
        except ValidationError as err:
            return err.messages, 422

        return {"message": "Your data is Successfully Updated!."}, 200
    else:
        return {"message": "User not found!."}, 401


def update_password():
    """
    This function use for update password
    """
    update_password_schema = UpdatePasswordSchema()
    json_data = request.get_json()
    if not bcrypt.check_password_hash(current_user.password, json_data["password"]):
        return {"message": "Invalid password!"}, 400
    # Validate and deserialize input
    try:
        data = update_password_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422
    new_password = bcrypt.generate_password_hash(data["new_password"]).decode("utf-8")
    current_user.password = new_password
    db.session.commit()
    return {"message": "Your password is Successfully Updated!."}, 200


def delete_user():
    """
    This function is user for delete user from all tables.This method only access by admin and HR
    """
    user_role = user_validation(get_jwt_identity())
    if user_role == 1 or user_role == 2:  # check user role
        json_data = request.get_json()
        userid = json_data["id"]
        user = User.query.get(userid)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted Successfully1!."}, 200

        else:
            return {"message": "User not found!."}, 401
    else:
        return {"message": "You don't have Credential to perform this action."}, 401
