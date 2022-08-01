from marshmallow import fields, Schema, post_load, INCLUDE, validates_schema, ValidationError, EXCLUDE
from office_management import ma
from office_management.users.models import User
from office_management.users.validators import email_validation


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class RegisterSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Email(required=True, validate=email_validation)
    password = fields.Str(required=True)
    role_id = fields.Int(required=False, default=4)
    is_active = fields.Boolean()

    class Meta:
        model = User
        include_fk = True
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs):
        del data["role_id"]
        return User(**data)


class UpdatePasswordSchema(Schema):
    password = fields.Str(required=True)
    new_password = fields.Str(required=True)
    confirm_password = fields.Str(required=True)

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if data["new_password"] != data["confirm_password"]:
            raise ValidationError("Your password is not match!.")


class UserProfileSchema(ma.SQLAlchemyAutoSchema):
    # firstname = fields.Str(required=False, default=None)
    # lastname = fields.Str(required=False, default=None)
    # phone = fields.Str(required=False, default=None)
    # birthday = fields.Date(required=False, default=None)
    # gender = fields.Str(required=False, default=None)
    # profile_image = fields.Str(required=False, default=None)

    class Meta:

        model = User
        unknown = INCLUDE
        load_instance = True
        ordered = True
        exclude = ("id", "password")

