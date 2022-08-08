from office_management.leaves.models import Leave, Holidays


def leave_check(leave_id):
    leave_get = Leave.query.filter_by(id=leave_id, status="pending").first()
    if leave_get:
        return True
    else:
        return False


def date_validation(date):
    arr = []
    holidays = Holidays.query.with_entities(Holidays.date).all()
    for i in holidays:
        arr.append(str(i[0]))
    if date in arr:
        return True
    else:
        return False

