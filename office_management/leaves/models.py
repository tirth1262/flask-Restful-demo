from datetime import datetime

from office_management import db


class Leave(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    start_date = db.Column(db.Date, index=True, nullable=False)
    end_date = db.Column(db.Date, index=True, nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.String(), default="pending")
    dept_user_id = db.Column(db.Integer, db.ForeignKey('department_user.id', ondelete="CASCADE"), nullable=False)


class LeaveComments(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    leave_id = db.Column(db.Integer, db.ForeignKey('leave.id', ondelete="CASCADE"), nullable=False)
    commenter_id = db.Column(db.Integer, db.ForeignKey('department_user.id', ondelete="CASCADE"), nullable=False)
    comment = db.Column(db.Text)
    time_stamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class LeaveStatus(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    leave_id = db.Column(db.Integer, db.ForeignKey('leave.id', ondelete="CASCADE"), nullable=False)
    approval_id = db.Column(db.Integer, db.ForeignKey('department_user.id', ondelete="CASCADE"), nullable=False)
    status = db.Column(db.String(50))
    time_stamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    leave = db.relationship("Leave", backref=db.backref("leave_status"), uselist=False)


class Holidays(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, index=True, nullable=False)


