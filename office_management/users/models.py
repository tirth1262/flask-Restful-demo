from office_management import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)


class UserRole(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", backref=db.backref("user_role"), uselist=False)

