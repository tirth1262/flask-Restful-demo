from office_management import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(50), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(128))


class UserRole(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", backref=db.backref("user_role", uselist=False))


class DepartmentUser(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id', ondelete="CASCADE"), nullable=False)
    user_role_id = db.Column(db.Integer, db.ForeignKey('user_role.id', ondelete="CASCADE"), nullable=False)
    user_role = db.relationship("UserRole", backref=db.backref("dept_user", uselist=False))


class UserHead(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    dept_user_id = db.Column(db.Integer, db.ForeignKey('department_user.id', ondelete="CASCADE"), nullable=False)
    head_id = db.Column(db.Integer, db.ForeignKey('department_user.id', ondelete="CASCADE"), default=1)
    dept_user = db.relationship("DepartmentUser", foreign_keys="[UserHead.head_id]",
                                backref=db.backref("user_head"), uselist=False)
