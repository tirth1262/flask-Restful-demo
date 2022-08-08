import re

from marshmallow import ValidationError

from office_management.constants import PASSWORD_REGEX
from office_management.roles.models import Role
from office_management.users.models import User, UserRole


def email_validation(email):
    user = User.query.filter_by(email=email).first()
    if user:
        raise ValidationError("email is already Registered, Please try with another email.")


def user_validation(user_id):
    user = UserRole.query.filter_by(user_id=user_id).first()
    role = Role.query.get(user.role_id)
    return role.name


def password_validation(password):
    reg = PASSWORD_REGEX
    pat = re.compile(reg)
    mat = re.search(pat, password)
    if not mat:
        raise ValidationError("Password is Invalid!.")


def validate_head(head):
    role_obj = UserRole.query.get()
    if not role_obj:
        raise ValidationError("Role is Not available!.")