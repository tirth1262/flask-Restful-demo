
from marshmallow import fields, Schema, post_load, INCLUDE, validates_schema, ValidationError, EXCLUDE
from office_management import ma
from office_management.users.models import User, UserHead
from office_management.users.validators import email_validation, password_validation


class UserSchema(Schema):
    """
        This Schema is used for login user
        It is take email and password and verified it.
    """
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class RegisterSchema(ma.SQLAlchemySchema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Email(required=True, validate=email_validation)
    password = fields.Str(required=True)
    role_id = fields.Int(required=False, default=4)
    dept_id = fields.Int(default=4)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        return password_validation(data["password"])

    class Meta:
        model = User
        include_fk = True
        load_instance = True
        unknown = EXCLUDE


class UpdatePasswordSchema(ma.SQLAlchemySchema):
    """
        THIS SCHEMA IS USED FOR UPDATE PASSWORD
    """
    password = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=password_validation)
    confirm_password = fields.Str(required=True)

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        """IT IS VALIDATE NEW-PASSWORD AND CONFIRM-PASSWORD IF BOTH IS NOT SAME THEN THOROUGH ERROR"""
        if data["new_password"] != data["confirm_password"]:
            raise ValidationError("Your password is not match!.")

        # return password_validation(data["password"])


class UserProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        unknown = INCLUDE
        load_instance = True
        ordered = True
        exclude = ("id", "password")


class UserHeadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserHead
        load_instance = True
        many = True
    # depth = 2



# class UpdateUserHeadSchema(ma.SQLAlchemySchema):


head_schema = UserHeadSchema(dump_only=("id",))
display_head_schema = UserHeadSchema(many=True)
