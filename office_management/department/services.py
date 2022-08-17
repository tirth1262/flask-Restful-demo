from http import HTTPStatus
from office_management import db
from office_management.constants import MSG_RETRIEVE_DEPARTMENTS, MSG_ADD_DEPARTMENT, MSG_RETRIEVE_DEPARTMENT, \
    ERR_DEPARTMENT_NOT_EXISTS, MSG_REGISTER_DEPARTMENT_UPDATED_SUCCESSFULLY, ERR_NO_DEPARTMENT_IN_DB
from office_management.department import Department
from office_management.department.schemas import add_dept_schema, delete_dept_schema, all_dept_schema, \
    update_dept_schema, dept_schema
from office_management.languages import Serializer, Response


class DeptServices:
    def __init__(self, request):
        self.request = request

    @staticmethod
    def get_all_department():
        """
        :return: ALL DEPARTMENTS WHICH ARE AVAILABLE IN DEPARTMENT TABLE
        """
        departments = Department.query.all()
        if departments:
            data = Serializer.dump(departments, all_dept_schema)
            return Response(status_code=HTTPStatus.OK, message=MSG_RETRIEVE_DEPARTMENTS,
                            data=data).send_success_response()

        return Response(status_code=HTTPStatus.BAD_REQUEST,
                        message=ERR_NO_DEPARTMENT_IN_DB).send_error_response()

    def add_dept(self):
        """
            THIS FUNCTION TAKE NEW_NAME AND ADD DEPARTMENT IN DEPARTMENT TABLE
            :return:  ADD NEW DEPARTMENT
        """
        is_true, data = Serializer.load(self.request, add_dept_schema)
        if is_true:
            new_dept = Department(name=data["name"])
            db.session.add(new_dept)
            db.session.commit()
            return Response(status_code=HTTPStatus.OK, message=MSG_ADD_DEPARTMENT) \
                .send_success_response()

        return Response(status_code=HTTPStatus.BAD_REQUEST,
                        message=data).send_error_response()

    def delete_dept(self):
        """
            THIS FUNCTION TAKE DEPARTMENT_ID AND DELETE DEPARTMENT IN DEPARTMENT TABLE
            :return:  DELETE DEPARTMENT
        """
        is_true, data = Serializer.load(self.request, delete_dept_schema)
        if is_true:
            dept_id = data["id"]
            dept = Department.query.get(dept_id)
            if dept:
                db.session.delete(dept)
                db.session.commit()
                return {"message": f"{dept.name} Department deleted Successfully!."}, 200
            else:
                return Response(status_code=HTTPStatus.BAD_REQUEST,
                                message=ERR_DEPARTMENT_NOT_EXISTS.format(dept_id)).send_error_response()
        return Response(status_code=HTTPStatus.BAD_REQUEST,
                        message=data).send_error_response()

    def update_dept(self):
        """
            THIS FUNCTION TAKE DEPARTMENT_ID,NEW_NAME AND UPDATE DEPARTMENT IN DEPARTMENT TABLE
            :return:  UPDATE DEPARTMENT
        """
        is_true, data = Serializer.load(self.request, update_dept_schema)
        if is_true:
            dept_id = data["id"]
            dept = Department.query.get(dept_id)
            if dept:
                dept.name = data["name"]
                db.session.commit()

                return Response(status_code=HTTPStatus.OK,
                                message=MSG_REGISTER_DEPARTMENT_UPDATED_SUCCESSFULLY).send_success_response()
            else:
                return Response(status_code=HTTPStatus.BAD_REQUEST,
                                message=ERR_DEPARTMENT_NOT_EXISTS.format(dept_id)).send_error_response()
        return Response(status_code=HTTPStatus.BAD_REQUEST,
                        message=data).send_error_response()

    @staticmethod
    def get_dept_by_id(dept_id):
        """
        :param dept_id: This is required to fetch particular DEPARTMENT
        :return: single DEPARTMENT object
        """
        dept = Department.query.get(dept_id)
        if dept:
            result = Serializer.dump(dept, dept_schema)
            return Response(status_code=HTTPStatus.OK, message=MSG_RETRIEVE_DEPARTMENT,
                            data=result).send_success_response()
        else:
            return Response(status_code=HTTPStatus.BAD_REQUEST,
                            message=ERR_DEPARTMENT_NOT_EXISTS.format(dept_id)).send_error_response()
