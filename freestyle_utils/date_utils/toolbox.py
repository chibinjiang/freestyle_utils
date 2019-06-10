import datetime


def get_utcnow(format=None):
    if format == 'iso':
        return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return datetime.datetime.utcnow()

