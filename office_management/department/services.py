from flask import request
from marshmallow import ValidationError
from office_management import db
from office_management.department import Department
from office_management.department.schemas import DepartmentSchema


def all_dept():
    """
    :return: ALL DEPARTMENTS WHICH ARE AVAILABLE IN DEPARTMENT TABLE
    """
    roles = Department.query.all()
    if roles:
        all_dept_schema = DepartmentSchema()
        result = all_dept_schema.dump(roles, many=True)
        return {'Departments': result}
    else:
        return {'msg': "No Departments available"}


def add_dept():
    """
        THIS FUNCTION TAKE NEW_NAME AND ADD DEPARTMENT IN DEPARTMENT TABLE
        :return:  ADD NEW DEPARTMENT
    """
    add_dept_schema = DepartmentSchema()
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    try:
        data = add_dept_schema.load(json_data, partial=("id",))
    except ValidationError as err:
        return err.messages, 422

    new_dept = Department(name=data["name"])
    db.session.add(new_dept)
    db.session.commit()
    return {'message': f'New {new_dept.name} named Department added successfully!.'}


def delete_dept():
    """
        THIS FUNCTION TAKE DEPARTMENT_ID AND DELETE DEPARTMENT IN DEPARTMENT TABLE
        :return:  DELETE DEPARTMENT
    """
    json_data = request.get_json()
    dept_schema = DepartmentSchema()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    try:
        data = dept_schema.load(json_data, partial=("name",))
    except ValidationError as err:
        return err.messages, 422
    dept_id = data["id"]
    dept = Department.query.get(dept_id)
    if dept:
        db.session.delete(dept)
        db.session.commit()
        return {"message": f"{dept.name} Department deleted Successfully!."}, 200
    else:
        return {"message": "Department not Found!."}, 401


def update_dept():
    """
        THIS FUNCTION TAKE DEPARTMENT_ID,NEW_NAME AND UPDATE DEPARTMENT IN DEPARTMENT TABLE
        :return:  UPDATE DEPARTMENT
    """
    json_data = request.get_json()
    dept_schema = DepartmentSchema()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    try:
        data = dept_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422
    dept_id = data["id"]
    dept = Department.query.get(dept_id)

    if dept:
        dept.name = data["name"]
        db.session.commit()
        return {"message": f"Department Updated Successfully!."}, 200
    else:
        return {"message": "Department not found!."}, 401
