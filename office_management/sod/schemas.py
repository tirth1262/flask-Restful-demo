from marshmallow import validates_schema, ValidationError
from office_management import ma
from office_management.sod import Sod
from office_management.sod.validation import sod_validation, sod_date_validation


class SodSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sod
        load_instance = True

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if not sod_validation(data["dept_user_id"]):
            raise ValidationError("Opps you haven't Added sod yet!.")

        if sod_date_validation(data["dept_user_id"], data["date"]):
            raise ValidationError("You already entered this day Sod, Please check it!.")


update_sod_schema = SodSchema(only=("id", "content"))
display_sod_schema = SodSchema()
add_sod_schema = SodSchema()
delete_sod_schema = SodSchema(only=("id",))
