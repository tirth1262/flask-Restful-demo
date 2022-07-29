from marshmallow import Schema, fields


class RoleSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)

