from marshmallow import Schema, fields
from office_management import ma
from office_management.roles.models import Role
from office_management.roles.validation import validate_role


class RoleSchema(ma.SQLAlchemySchema):
    id = fields.Int(required=True, validate=validate_role)
    name = fields.Str(required=True)

    class Meta:
        model = Role
        load_instance = True


display_roles_schema = RoleSchema(many=True)
add_role_schema = RoleSchema(partial=("id",))
delete_role_schema = RoleSchema(partial=("name",))
update_role_schema = RoleSchema()
display_role_schema = RoleSchema()
