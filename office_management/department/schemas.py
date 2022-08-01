from marshmallow import Schema, fields


class DepartmentSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
