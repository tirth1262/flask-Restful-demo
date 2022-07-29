from datetime import datetime

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
    user_profile = db.relationship("UserProfile", backref=db.backref("user"), uselist=False)


class Role(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(50), nullable=True)


class UserRole(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", backref=db.backref("user_role"), uselist=False)



class UserProfile(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    profile_image = db.Column(db.String(200), nullable=True, default='http://res.cloudinary.com/dfmukiaes/image'
                                                                     '/upload/v1657186897/Profile_images'
                                                                     '/ndo0gjrywo4yawbhxwqi.jpg')
    birthday = db.Column(db.Date, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)


class OfficialInformation(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    join_date = db.Column(db.Date, nullable=True, default=datetime.utcnow)
    experience = db.Column(db.String(120), nullable=True)
    skype_id = db.Column(db.String(120), nullable=True)
    gitlab_id = db.Column(db.String(120), nullable=True)
    github_id = db.Column(db.String(120), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)


class PersonalInfo(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    blood_group = db.Column(db.String(20), nullable=True)
    marital_status = db.Column(db.String(20), nullable=True)
    emergency_number = db.Column(db.String(20), nullable=True)
    current_address = db.Column(db.Text, nullable=True)
    permanent_address = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)


