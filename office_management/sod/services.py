from http import HTTPStatus
from flask_jwt_extended import current_user
from sqlalchemy import desc
from office_management import db
from office_management.constants import MSG_RETRIEVE_ROLES, MSG_RETRIEVE_SOD, MSG_DELETED_SOD, \
    MSG_REGISTER_SOD_UPDATED_SUCCESSFULLY, MSG_SOD_ADD, ERR_NO_SOD_IN_DB, ERR_NO_ACCESS_SOD, ERR_SOD_NOT_EXISTS
from office_management.languages import Serializer, Response
from office_management.sod import Sod
from office_management.sod.schemas import display_sod_schema, add_sod_schema, update_sod_schema, delete_sod_schema


class SodServices:
    def __init__(self, request):
        self.request = request

    def add_sod(self):
        current_user_dept_id = current_user.user_role.dept_user.id
        is_true, data = Serializer.load(self.request, add_sod_schema)
        if is_true:
            new_sod = Sod(content=data["content"], dept_user_id=current_user_dept_id, date=data["date"])
            db.session.add(new_sod)
            db.session.commit()
            return Response(status_code=HTTPStatus.OK, message=MSG_SOD_ADD).send_success_response()
        return Response(status_code=HTTPStatus.BAD_REQUEST, message=data).send_error_response()

    @staticmethod
    def get_all_sod():
        current_user_dept_id = current_user.user_role.dept_user.id
        sod = Sod.query.filter_by(dept_user_id=current_user_dept_id).order_by(desc(Sod.date)).all()
        if sod:
            result = Serializer.dump(sod, display_sod_schema)
            return Response(status_code=HTTPStatus.OK, message=MSG_RETRIEVE_ROLES,
                            data=result).send_success_response()
        return Response(status_code=HTTPStatus.BAD_REQUEST, message=ERR_NO_SOD_IN_DB).send_error_response()

    def delete_sod(self):
        is_true, data = Serializer.load(self.request, delete_sod_schema)
        if is_true:
            sod = Sod.query.get(data["id"])
            db.session.delete(sod)
            db.session.commit()
            return Response(status_code=HTTPStatus.OK, message=MSG_DELETED_SOD).send_success_response()
        return Response(status_code=HTTPStatus.BAD_REQUEST, message=data).send_error_response()

    def update_sod(self):
        is_true, data = Serializer.load(self.request, update_sod_schema)
        if is_true:
            sod_id = data["id"]
            sod = Sod.query.get(sod_id)
            sod.content = data["content"]
            db.session.commit()
            return Response(status_code=HTTPStatus.OK,
                            message=MSG_REGISTER_SOD_UPDATED_SUCCESSFULLY).send_success_response()
        return Response(status_code=HTTPStatus.BAD_REQUEST, message=data).send_error_response()

    @staticmethod
    def get_sod_by_id(sod_id):
        current_user_dept_id = current_user.user_role.dept_user.id
        sod = Sod.query.get(sod_id)
        if sod:
            if sod.dept_user_id == current_user_dept_id:
                return Response(status_code=HTTPStatus.OK, message=MSG_RETRIEVE_SOD,
                                data=sod).send_success_response()
            return Response(status_code=HTTPStatus.BAD_REQUEST, message=ERR_NO_ACCESS_SOD).send_error_response()
        return Response(status_code=HTTPStatus.BAD_REQUEST, message=ERR_SOD_NOT_EXISTS).send_error_response()
