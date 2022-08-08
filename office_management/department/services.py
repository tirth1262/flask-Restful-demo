from http import HTTPStatus
from office_management import db
from office_management.constants import MSG_RETRIEVE_DEPARTMENTS, MSG_ADD_DEPARTMENT
from office_management.department import Department
from office_management.department.schemas import add_dept_schema, delete_dept_schema, all_dept_schema, \
    update_dept_schema
from office_management.languages import Serializer, Response


class DeptServices:
    def __init__(self, request):
        self.request = request

    @staticmethod
    def all_dept():
        """
        :return: ALL DEPARTMENTS WHICH ARE AVAILABLE IN DEPARTMENT TABLE
        """
        departments = Department.query.all()
        if departments:
            data = Serializer.dump(departments, all_dept_schema)
            return Response(status_code=HTTPStatus.OK, message=MSG_RETRIEVE_DEPARTMENTS,
                            data=data).send_success_response()

        return Response(status_code=HTTPStatus.BAD_REQUEST,
                        message="No Departments available NOW.").send_error_response()

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
                return {"message": "Department not Found!."}, 401
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
                return {"message": f"Department Updated Successfully!."}, 200
            else:
                return {"message": "Department not found!."}, 401
        return Response(status_code=HTTPStatus.BAD_REQUEST,
                        message=data).send_error_response()
