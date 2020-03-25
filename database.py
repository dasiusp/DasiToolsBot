from google.cloud import firestore

db = firestore.Client()


def get_reminder_date():
    func = db.collection('dasi_groups').document('reminder_date').get()
    return func


def get_allowed_groups():
    allowed_groups = db.collection('dasi_groups').document('allowed_groups').get()
    return allowed_groups


def update_reminder_date(date):
    current_reminder = {
        'year': date.year,
        'month': date.month,
        'day': date.day
    }
    db.collection('dasi_groups').document('reminder_date').set(current_reminder)


def join_group_list(group_name, user_id, username):
    db.collection('dasi_groups').document(str(group_name)).update({str(user_id): username})
    db.collection('dasi_groups').document('Todos').update({str(user_id): username})


def get_group_list(group_name):
    group_list = db.collection('dasi_groups').document(str(group_name)).get()
    return group_list
