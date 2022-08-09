from marshmallow import Schema, fields, validates_schema, ValidationError
from office_management import ma
from office_management.leaves.models import LeaveStatus, Leave, Holidays, LeaveComments
from office_management.leaves.utils import leave_check, date_validation


class LeaveSchema(Schema):
    id = fields.Int(required=False)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    reason = fields.Str(required=True)
    status = fields.Str()

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if data["start_date"] > data["end_date"]:
            raise ValidationError("Please select a valid end date.")
        if not date_validation(data["start_date"]):
            raise ValidationError("On this date already holiday declared!.")
        if not date_validation(data["end_date"]):
            raise ValidationError("On this date already holiday declared!.")


class LeaveCommentSchema(ma.SQLAlchemySchema):
    id = fields.Int(dump_only=True)
    leave_id = fields.Int(required=True)
    comment = fields.Str(required=True)
    time_stamp = fields.Date(dump_only=True)

    class Meta:
        model = LeaveComments
        load_instance = True


class leaveApprovalSchema(Schema):
    id = fields.Int(dump_only=True)
    leave_id = fields.Int(required=True)
    approval_id = fields.Int(dump_only=True)
    status = fields.Str(required=True)
    time_stamp = fields.Date(dump_only=True)

    class Meta:
        model = LeaveStatus


class LeaveUpdateSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Leave
        load_instance = True
        ordered = True
        dump_only = ("status", "dept_user_id")

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if data["start_date"] < data["end_date"]:
            raise ValidationError("Please select a valid end date.")

        if not leave_check(data["id"]):
            raise ValidationError("You can not update this leave Request!.")


class HolidaySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Holidays
        load_instance = True
        ordered = True


leave_schema = LeaveSchema(many=True)
leave_comment_schema = LeaveCommentSchema()
add_leave_schema = LeaveSchema()



holidays_schema = HolidaySchema(many=True)
add_holidays_schema = HolidaySchema()
delete_holidays_schema = HolidaySchema(partial=("name", "date"))