from http import HTTPStatus
from office_management import db
from office_management.constants import MSG_RETRIEVE_ROLES, MSG_RETRIEVE_ROLE, ERR_ROLE_NOT_EXISTS, MSG_ROLE_ADD, \
    ERR_NO_ROLE_IN_DB, MSG_DELETED_ROLE
from office_management.roles.schemas import display_roles_schema, add_role_schema, delete_role_schema, \
    update_role_schema, display_role_schema
from office_management.roles.models import Role
from office_management.languages import Serializer, Response


class RoleServices:
    def __init__(self, request):
        self.request = request

    def create_role(self):
        """
            THIS FUNCTION TAKE NAME AND ADD NEW ROLES IN ROLES TABLE
            :return: CREATE NEW ROLE
            """
        is_true, data = Serializer.load(self.request, add_role_schema)
        if is_true:
            new_role = Role(name=data.name)
            db.session.add(new_role)
            db.session.commit()
            return Response(status_code=HTTPStatus.OK, message=MSG_ROLE_ADD).send_success_response()
        return Response(status_code=HTTPStatus.BAD_REQUEST, message=data).send_error_response()

    @staticmethod
    def get_all_roles():
        """
        THIS FUNCTION FETCH ALL ROLES FROM ROLES TABLE
        :return: ALL ROLES
        """
        roles = Role.query.all()
        if roles:
            result = Serializer.dump(roles, display_roles_schema)

            return Response(status_code=HTTPStatus.OK, message=MSG_RETRIEVE_ROLES,
                            data=result).send_success_response()

        return Response(status_code=HTTPStatus.BAD_REQUEST, message=ERR_NO_ROLE_IN_DB).send_error_response()

    def delete_role(self):
        """
            THIS FUNCTION TAKE ROLE ID AND DELETE ROLE IN ROLES TABLE
            :return:  DELETE ROLE
        """
        is_true, data = Serializer.load(self.request, delete_role_schema)
        if is_true:
            role = Role.query.get(data["id"])
            db.session.delete(role)
            db.session.commit()
            return Response(status_code=HTTPStatus.OK, message=MSG_DELETED_ROLE).send_success_response()
        return Response(status_code=HTTPStatus.BAD_REQUEST, message=data).send_error_response()

    def update_role(self):
        """
            THIS FUNCTION TAKE ROLE_ID,NEW_NAME AND UPDATE ROLE IN ROLES TABLE
            :return:  UPDATE ROLE
        """
        is_true, data = Serializer.load(self.request, update_role_schema)
        if is_true:
            role = Role.query.get(data.id)
            role.name = data.name
            # db.session.commit()
            return Response(status_code=HTTPStatus.OK, message=MSG_DELETED_ROLE).send_success_response()

        return Response(status_code=HTTPStatus.BAD_REQUEST, message=data).send_error_response()

    @staticmethod
    def get_role_by_id(role_id):
        """

        :param role_id: This is required to fetch particular role
        :return: single role object
        """
        role = Role.query.get(role_id)
        if role:
            result = Serializer.dump(role, display_role_schema)
            return Response(status_code=HTTPStatus.OK, message=MSG_RETRIEVE_ROLE,
                            data=result).send_success_response()
        else:
            return Response(status_code=HTTPStatus.BAD_REQUEST,
                            message=ERR_ROLE_NOT_EXISTS.format(role_id)).send_error_response()
