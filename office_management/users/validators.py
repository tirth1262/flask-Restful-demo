from marshmallow import ValidationError
from office_management.users.models import User


def email_validation(email):
    user = User.query.filter_by(email=email).first()
    if user:
        raise ValidationError("email is already Registered, Please try with another email.")


def user_validation(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user.role
