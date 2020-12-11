import datetime


def str_is_empty(str):
    return (str is None) or (str == "") or (str.strip() == "")


def str_trim(str):
    return None if str_is_empty(str) else str.strip()


def datetime_to_iso8601(date):
    return date.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=8)), microsecond=0).isoformat()
