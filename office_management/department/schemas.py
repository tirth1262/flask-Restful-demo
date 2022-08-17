from marshmallow import Schema, fields


class DepartmentSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)


all_dept_schema = DepartmentSchema(many=True)
add_dept_schema = DepartmentSchema(partial=("id",))
delete_dept_schema = DepartmentSchema(partial=("name",))
update_dept_schema = DepartmentSchema()
dept_schema = DepartmentSchema()
