from marshmallow import validates_schema, ValidationError
from office_management import ma
from office_management.eod.validation import eod_validation, eod_date_validation
from office_management.sod import Sod


class EodSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sod
        load_instance = True

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if not eod_validation(data["dept_user_id"]):
            raise ValidationError("Opps you haven't Added sod yet!.")

        if eod_date_validation(data["dept_user_id"], data["date"]):
            raise ValidationError("You already entered this day Sod, Please check it!.")


update_eod_schema = EodSchema(only=("id", "content"))
display_eod_schema = EodSchema()
add_eod_schema = EodSchema()
delete_eod_schema = EodSchema(only=("id",))
