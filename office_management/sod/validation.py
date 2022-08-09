from office_management.sod import Sod


def sod_validation(sod_id):
    sod = Sod.query.get(sod_id)
    if sod:
        return True
    else:
        return False


def sod_date_validation(user_id, date):
    sod = Sod.query.filter_by(dept_user_id=user_id, date=date).first()
    if sod:
        return True
    else:
        return False
