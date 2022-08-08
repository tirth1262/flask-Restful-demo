from marshmallow import ValidationError

from office_management.roles.models import Role


def validate_role(role):
    role_obj = Role.query.get(role)
    if not role_obj:
        raise ValidationError("Role is Not available!.")