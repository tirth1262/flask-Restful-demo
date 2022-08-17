from office_management.eod import Eod


def eod_validation(sod_id):
    eod = Eod.query.get(sod_id)
    if eod:
        return True
    else:
        return False


def eod_date_validation(user_id, date):
    eod = Eod.query.filter_by(dept_user_id=user_id, date=date).first()
    if eod:
        return True
    else:
        return False
