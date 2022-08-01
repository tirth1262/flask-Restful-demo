from office_management import db


class Department(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class DepartmentUser(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id', ondelete="CASCADE"), nullable=False)
    user_role_id = db.Column(db.Integer, db.ForeignKey('user_role.id', ondelete="CASCADE"), nullable=False)
