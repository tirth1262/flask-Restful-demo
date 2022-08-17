from http import HTTPStatus
from flask_jwt_extended import current_user
from sqlalchemy import desc
from office_management import db
from office_management.constants import MSG_RETRIEVE_ROLES, ERR_NO_EOD_IN_DB, MSG_DELETED_EOD, MSG_RETRIEVE_EOD, \
    ERR_EOD_NOT_EXISTS, ERR_NO_ACCESS_EOD, MSG_REGISTER_EOD_UPDATED_SUCCESSFULLY, MSG_EOD_ADD
from office_management.eod import Eod
from office_management.languages import Serializer, Response
from office_management.sod import Sod
from office_management.eod.schemas import display_eod_schema, add_eod_schema, update_eod_schema, delete_eod_schema


class EodServices:
    def __init__(self, request):
        self.request = request

    def add_eod(self):
        # "current_user_dept_id" is a departmentUser id of current user
        current_user_dept_id = current_user.user_role.dept_user.id
        is_true, data = Serializer.load(self.request, add_eod_schema)
        if is_true:
            new_sod = Sod(content=data["content"], dept_user_id=current_user_dept_id, date=data["date"])
            db.session.add(new_sod)
            db.session.commit()
            return Response(status_code=HTTPStatus.OK, message=MSG_EOD_ADD).send_success_response()
        return Response(status_code=HTTPStatus.BAD_REQUEST, message=data).send_error_response()

    @staticmethod
    def get_all_eod():

        current_user_dept_id = current_user.user_role.dept_user.id
        eod = Eod.query.filter_by(dept_user_id=current_user_dept_id).order_by(desc(Sod.date)).all()
        if eod:
            result = Serializer.dump(eod, display_eod_schema)
            return Response(status_code=HTTPStatus.OK, message=MSG_RETRIEVE_ROLES,
                            data=result).send_success_response()
        return Response(status_code=HTTPStatus.BAD_REQUEST, message=ERR_NO_EOD_IN_DB).send_error_response()

    def delete_eod(self):

        is_true, data = Serializer.load(self.request, delete_eod_schema)
        if is_true:
            eod = Eod.query.get(data["id"])
            db.session.delete(eod)
            db.session.commit()
            return Response(status_code=HTTPStatus.OK, message=MSG_DELETED_EOD).send_success_response()
        return Response(status_code=HTTPStatus.BAD_REQUEST, message=data).send_error_response()

    def update_eod(self):
        is_true, data = Serializer.load(self.request, update_eod_schema)
        if is_true:
            eod = Sod.query.get(data["id"])
            eod.content = data["content"]
            db.session.commit()
            return Response(status_code=HTTPStatus.OK,
                            message=MSG_REGISTER_EOD_UPDATED_SUCCESSFULLY).send_success_response()
        return Response(status_code=HTTPStatus.BAD_REQUEST, message=data).send_error_response()

    @staticmethod
    def get_eod_by_id(eod_id):
        current_user_dept_id = current_user.user_role.dept_user.id
        eod = Eod.query.get(eod_id)
        if eod:
            if eod.dept_user_id == current_user_dept_id:
                return Response(status_code=HTTPStatus.OK, message=MSG_RETRIEVE_EOD,
                                data=eod).send_success_response()
            return Response(status_code=HTTPStatus.BAD_REQUEST, message=ERR_NO_ACCESS_EOD).send_error_response()
        return Response(status_code=HTTPStatus.BAD_REQUEST, message=ERR_EOD_NOT_EXISTS).send_error_response()
