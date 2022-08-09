from office_management import db


class Sod(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    dept_user_id = db.Column(db.Integer, db.ForeignKey('department_user.id', ondelete="CASCADE"), nullable=False)
    content = db.Column(db.Text)
    date = db.Column(db.Date, index=True, nullable=False)