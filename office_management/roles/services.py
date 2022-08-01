from flask import request
from marshmallow import ValidationError
from office_management import db
from office_management.roles.schemas import RoleSchema
from office_management.roles.models import Role


def all_roles():
    """
    THIS FUNCTION FETCH ALL ROLES FROM ROLES TABLE
    :return: ALL ROLES
    """
    roles = Role.query.all()
    if roles:
        all_roles_schema = RoleSchema()
        result = all_roles_schema.dump(roles, many=True)
        return {'Roles': result}
    else:
        return {'msg': "No role available"}


def add_role():
    """
        THIS FUNCTION TAKE NAME AND ADD NEW ROLES IN ROLES TABLE
        :return: CREATE NEW ROLE
        """
    add_role_schema = RoleSchema()
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    try:
        data = add_role_schema.load(json_data, partial=("id",))
    except ValidationError as err:
        return err.messages, 422

    new_role = Role(name=data["name"])
    db.session.add(new_role)
    db.session.commit()
    return {'message': 'New role added successfully!.'}


def delete_role():
    """
        THIS FUNCTION TAKE ROLE ID AND DELETE ROLE IN ROLES TABLE
        :return:  DELETE ROLE
    """
    json_data = request.get_json()
    role_schema = RoleSchema()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    try:
        data = role_schema.load(json_data, partial=("name",))
    except ValidationError as err:
        return err.messages, 422
    role_id = data["id"]
    role = Role.query.get(role_id)
    if role:
        db.session.delete(role)
        db.session.commit()
        return {"message": "Role deleted Successfully1!."}, 200
    else:
        return {"message": "Role not Found!."}, 401


def update_role():
    """
        THIS FUNCTION TAKE ROLE_ID,NEW_NAME AND UPDATE ROLE IN ROLES TABLE
        :return:  UPDATE ROLE
    """
    json_data = request.get_json()
    role_schema = RoleSchema()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    try:
        data = role_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422
    role_id = data["id"]
    role = Role.query.get(role_id)

    if role:
        role.name = data["name"]
        db.session.commit()
        return {"message": "Role Updated Successfully!."}, 200
    else:
        return {"message": "Role not found!."}, 401


