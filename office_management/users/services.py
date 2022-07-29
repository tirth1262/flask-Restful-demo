from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, current_user, create_refresh_token
from marshmallow import ValidationError
from office_management import db, bcrypt, jwt
from office_management.users.models import User, UserProfile, PersonalInfo, OfficialInformation, UserRole
from office_management.users.schemas import (UserSchema, RegisterSchema,
                                             UserProfileSchema, OfficialInformationSchema,
                                             PersonalInfoSchema, UpdatePasswordSchema)
from office_management.users.validators import user_validation



@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


def login():
    quote_schema = UserSchema()
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    try:
        data = quote_schema.load(json_data)
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
    access_token = create_access_token(identity=user.id, additional_claims={"role": f'{user.user_role[0].role_id}'})
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


def refresh():
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
        new_profile = UserProfile(user_id=data.id)
        new_personal_info = PersonalInfo(user_id=data.id)
        new_official_info = OfficialInformation(user_id=data.id)
        new_role = UserRole(user_id=data.id, role_id=json_data["role_id"])
        db.session.add(new_official_info)
        db.session.add(new_profile)
        db.session.add(new_personal_info)
        db.session.add(new_role)
        db.session.commit()
        return {"message": f"{data.username} named new user created Successfully."}, 200
    else:
        return {"message": "You don't have Credential to perform this action."}, 401


# THIS FUNCTION GET CURRENT USER DATA FROM USER PROFILE TABLE
def user_profile():
    user = User.query.filter_by(id=get_jwt_identity()).first()
    if user:
        user_profile_schema = UserProfileSchema()
        result = user_profile_schema.dump(user)
        return {"User": result}
    else:
        return {"message": "User no found!."}, 401


def update_user_profile():
    """
    THIS FUNCTION IS UPDATE USER PROFILE TABLE AND UPDATE DATA IN USER PROFILE TABLE
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
            # Due to "instance" pass in load auto object add in user Profile Model
            data = user_profile_schema.load(json_data, instance=profile_of_user)
            db.session.commit()
        except ValidationError as err:
            return err.messages, 422

        return {"message": "Your data is Successfully Updated!."}, 200
    else:
        return {"message": "User not found!."}, 401


def update_official_profile():
    """
    THIS FUNCTION IS UPDATE OFFICIAL PROFILE TABLE AND UPDATE DATA IN USER OFFICIAL-INFORMATION TABLE
    """
    user_id = get_jwt_identity()
    official_profile_of_user = OfficialInformation.query.filter_by(user_id=user_id).first()
    if official_profile_of_user:
        user_off_profile_schema = OfficialInformationSchema()
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        # Validate and deserialize input
        try:
            data = user_off_profile_schema.load(json_data, instance=official_profile_of_user)
            db.session.commit()
        except ValidationError as err:
            return err.messages, 422

        return {"message": "Your data is Successfully Updated!."}, 200
    else:
        return {"message": "User not found!."}, 401


def user_official_profile():
    user_id = get_jwt_identity()
    user = OfficialInformation.query.filter_by(user_id=user_id).first()
    if user:
        user_profile_schema = OfficialInformationSchema()
        result = user_profile_schema.dump(user)
        return {"User": result}
    else:
        return {"message": "User not found!."}, 401


def update_personal_profile():
    user_id = get_jwt_identity()
    personal_profile_of_user = PersonalInfo.query.filter_by(user_id=user_id).first()
    if personal_profile_of_user:
        user_per_profile_schema = PersonalInfoSchema()
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        # Validate and deserialize input
        try:
            data = user_per_profile_schema.load(json_data, instance=personal_profile_of_user)
            db.session.commit()
        except ValidationError as err:
            return err.messages, 422

        return {"message": "Your data is Successfully Updated!."}, 200
    else:
        return {"message": "User not found!."}, 401


def user_personal_profile():
    user_id = get_jwt_identity()
    user = PersonalInfo.query.filter_by(user_id=user_id).first()
    if user:
        personal_profile_schema = PersonalInfoSchema()
        result = personal_profile_schema.dump(user)
        return {"User": result}
    else:
        return {"message": "User not found!."}, 401


def update_password():
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
    if user_role == "admin" or user_role == "HR":  # check user role
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
