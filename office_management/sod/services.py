from http import HTTPStatus
from flask_jwt_extended import current_user
from sqlalchemy import desc
from office_management import db
from office_management.constants import MSG_RETRIEVE_ROLES
from office_management.roles.models import Role
from office_management.languages import Serializer, Response
from office_management.sod import Sod
from office_management.sod.schemas import display_sod_schema, add_sod_schema, update_sod_schema, delete_sod_schema


class SodServices:
    def __init__(self, request):
        self.request = request

    def add_sod(self):
        """
            THIS FUNCTION TAKE NAME AND ADD NEW ROLES IN ROLES TABLE
            :return: CREATE NEW ROLE
            """
        # "current_user_dept_id" is a departmentUser id of current user
        current_user_dept_id = current_user.user_role.dept_user.id
        is_true, data = Serializer.load(self.request, add_sod_schema)
        if is_true:
            new_sod = Sod(content=data["content"], dept_user_id=current_user_dept_id, date=data["date"])
            db.session.add(new_sod)
            db.session.commit()
            return {'message': 'Your SOD added successfully!.'}
        return Response(status_code=HTTPStatus.BAD_REQUEST, message=data).send_error_response()

    @staticmethod
    def display_sod():
        """
        THIS FUNCTION FETCH ALL ROLES FROM ROLES TABLE
        :return: ALL ROLES
        """
        current_user_dept_id = current_user.user_role.dept_user.id
        sod = Sod.query.filter_by(dept_user_id=current_user_dept_id).order_by(desc(Sod.date)).all()
        if sod:
            result = Serializer.dump(sod, display_sod_schema)
            return Response(status_code=HTTPStatus.OK, message=MSG_RETRIEVE_ROLES,
                            data=result).send_success_response()
        return Response(status_code=HTTPStatus.BAD_REQUEST, message="No Roles to display").send_error_response()

    def delete_sod(self):
        """
            THIS FUNCTION TAKE SOD ID AND DELETE SOD IN SOD TABLE
            :return:  DELETE SOD
        """
        is_true, data = Serializer.load(self.request, delete_sod_schema)
        if is_true:
            sod = Sod.query.get(data["id"])
            db.session.delete(sod)
            db.session.commit()
            return {"message": "Sod deleted Successfully1!."}, 200
        return Response(status_code=HTTPStatus.BAD_REQUEST, message=data).send_error_response()

    def update_sod(self):
        """
            THIS FUNCTION TAKE ROLE_ID,NEW_NAME AND UPDATE ROLE IN ROLES TABLE
            :return:  UPDATE ROLE
        """
        is_true, data = Serializer.load(self.request, update_sod_schema)
        if is_true:
            sod_id = data["id"]
            sod = Sod.query.get(sod_id)
            sod.content = data["content"]
            db.session.commit()
            return {"message": "Sod Updated Successfully!."}, 200

        return Response(status_code=HTTPStatus.BAD_REQUEST, message=data).send_error_response()


