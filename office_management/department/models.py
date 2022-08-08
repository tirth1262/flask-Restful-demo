from office_management import db


class Department(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)



