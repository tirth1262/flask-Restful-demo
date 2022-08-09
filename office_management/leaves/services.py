from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, current_user
from flask import request
from marshmallow import ValidationError
from office_management import db, jwt
from office_management.constants import MSG_RETRIEVE_Leaves, MSG_LEAVE_REQUEST, MSG_COMMENT_ADD, MSG_NO_HOLIDAYS, \
    MSG_HOLIDAY_ADD
from office_management.languages import Serializer, Response
from office_management.leaves.models import Leave, LeaveStatus, LeaveComments, Holidays
from office_management.leaves.schemas import leaveApprovalSchema, HolidaySchema, \
    leave_schema, leave_comment_schema, add_leave_schema, holidays_schema, add_holidays_schema, delete_holidays_schema
from office_management.users.models import UserHead, User
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


def display_user_leaves():
    """
    Display current user all leave requests
    :return: Fetch all lEAVE requests from Leave table of current user
    """
    # "current_user_dept_id" is a departmentUser id of current user
    current_user_dept_id = current_user.user_role.dept_user.id
    leaves = Leave.query.filter_by(dept_user_id=current_user_dept_id).all()
    if leaves:
        result = Serializer.dump(leaves, leave_schema)
        for i in result:
            i["username"] = current_user.username
        return Response(status_code=HTTPStatus.OK, message=MSG_RETRIEVE_Leaves,
                        data=result).send_success_response()

    return Response(status_code=HTTPStatus.BAD_REQUEST, message="No Leaves to display").send_error_response()


def leave_request():
    """
    This function is used for applied for leave request
    :return: It's ADD NEW LEAVE REQUEST OF CURRENT USER with validation
    """
    # "current_user_dept_id" is a departmentUser id of current user
    current_user_dept_id = current_user.user_role.dept_user.id
    is_true, data = Serializer.load(request, add_leave_schema)
    if is_true:
        new_leave = Leave(start_date=data['start_date'], end_date=data["end_date"],
                          reason=data["reason"], dept_user_id=current_user_dept_id)
        db.session.add(new_leave)
        # db.session.commit()
        return Response(status_code=HTTPStatus.OK, message=MSG_LEAVE_REQUEST).send_success_response()

    return Response(status_code=HTTPStatus.BAD_REQUEST, message=data).send_error_response()


def leave_update():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    leave_obj = Leave.query.filter_by(id=json_data["id"], status="pending").first()
    # Validate and deserialize input
    try:
        leave_schema.load(json_data, instance=leave_obj)
        db.session.commit()
        return {"message": "Your leave Has been Updated!."}
    except ValidationError as err:
        return err.messages, 422


def all_pending_request():
    user_role = user_validation(get_jwt_identity())
    """
        Check first user role if admin(1) or Hr(2) then fetch all leave requests
    """
    if user_role == "admin" or user_role == "hr":  # check user role
        all_leave = Leave.query.filter_by(status="pending").all()
        try:
            data = leave_schema.dump(all_leave, many=True)
        except ValidationError as err:
            return err.messages, 422
        if data:
            return {"Leaves": data}
        else:
            return {"message": "No leave Requests available Now."}

    elif user_role == "team-leader":
        """
            If user role is 3 (TL-TEAM LEADER) THEN FETCH ONLY THOSE REQUEST 
            WHICH ARE WHICH USER HEAD IS THAT TL.
        """

        """
            "all_consultant" QUERY FIRST FETCH ALL USER ID WHICH HEAD CURRENT TL AND APPEND IN A LIST
        """
        all_consultant = UserHead.query.with_entities(UserHead.user_id)\
            .filter_by(head_id=get_jwt_identity(), status="pending").all()
        all_consultant_list = []
        for i in all_consultant:
            all_consultant_list.append(i[0])
        """
            "all_leaves" QUERY FETCH ONLY THOSE LEAVE REQUEST WHICH USER_ID IN "all_consultant_list"
        """
        all_leaves = Leave.query.filter(Leave.user_id.in_(all_consultant_list)).all()
        try:
            data = leave_schema.dump(all_leaves, many=True)
        except ValidationError as err:
            return err.messages, 422
        if data:
            return {"Leaves": data}
        else:
            return {"message": "No leave available Now."}


def leave_action():
    leave_action_schema = leaveApprovalSchema()
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    try:
        data = leave_action_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422

    new_status = LeaveStatus(leave_id=data["leave_id"], approval_id=get_jwt_identity(), status=data["status"])
    db.session.add(new_status)
    db.session.commit()

    # check = LeaveStatus.query.filter_by(leave_id=data["leave_id"]).all()


"""----------------------------Leave comment-------------------"""


def leave_comment():
    is_true, data = Serializer.load(request, leave_comment_schema)
    if is_true:
        new_comment = LeaveComments(leave_id=data["leave_id"],
                                    commenter_id=get_jwt_identity(), comment=data["comment"])
        db.session.add(new_comment)
        db.session.commit()
        return Response(status_code=HTTPStatus.OK, message=MSG_COMMENT_ADD.send_success_response())

    return Response(status_code=HTTPStatus.BAD_REQUEST, message=data).send_error_response()


def display_comments():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    comments = LeaveComments.query.filter_by(leave_id=json_data["leave_id"]).all()
    # Validate and deserialize input
    try:
        data = leave_comment_schema.dump(comments)
    except ValidationError as err:
        return err.messages, 422

    return {"Comments": data}



"""-----------------------------Holidays------------------------------------"""

def display_holidays():
    """
    THIS FUNCTION FETCH ALL ROLES FROM ROLES TABLE
    :return: ALL ROLES
    """
    holidays = Holidays.query.all()
    if holidays:
        data = Serializer.dump(holidays, holidays_schema)
        return Response(status_code=HTTPStatus.OK, data=data, message=MSG_COMMENT_ADD.send_success_response())
    else:
        return Response(status_code=HTTPStatus.BAD_REQUEST, message=MSG_NO_HOLIDAYS).send_error_response()


def add_holiday():
    """
        THIS FUNCTION TAKE NAME AND ADD NEW ROLES IN ROLES TABLE
        :return: CREATE NEW ROLE
        """

    is_true, data = Serializer.load(request, add_holidays_schema)
    if is_true:
        new_holiday = Holidays(name=data.name, date=data.date)
        db.session.add(new_holiday)
        db.session.commit()
        return Response(status_code=HTTPStatus.OK, message=MSG_HOLIDAY_ADD.send_success_response())

    return Response(status_code=HTTPStatus.BAD_REQUEST, message=data).send_error_response()


def delete_holiday():
    """
        THIS FUNCTION TAKE ROLE ID AND DELETE ROLE IN ROLES TABLE
        :return:  DELETE ROLE
    """

    is_true, data = Serializer.load(request, delete_holidays_schema)
    if is_true:
    # holiday_id = data["id"]
        holiday = Holidays.query.get(data["id"])
        if holiday:
            db.session.delete(holiday)
            db.session.commit()
            return {"message": "Role deleted Successfully1!."}, 200
        else:
            return {"message": "Role not Found!."}, 401
    return Response(status_code=HTTPStatus.BAD_REQUEST, message=data).send_error_response()

def update_holiday():
    """
        THIS FUNCTION TAKE ROLE_ID,NEW_NAME AND UPDATE ROLE IN ROLES TABLE
        :return:  UPDATE ROLE
    """
    json_data = request.get_json()
    holidays_schema = HolidaySchema()

    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    holiday = Holidays.query.get(json_data["id"])
    try:
        holidays_schema.load(json_data, instance=holiday)
        db.session.commit()
        return {"message": "Holiday Updated Successfully!."}, 200
    except ValidationError as err:
        return err.messages, 422
