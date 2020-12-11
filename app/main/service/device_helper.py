"""
    For device data helper
"""
from app.main.util.conv import str_trim


def get_cust_user_device(user_demand):
    user_name = str_trim(user_demand.get("user"))
    max_device = user_demand.get("max_device")
    if max_device is None or max_device < 0:
        device_number = 10
    else:
        device_number = max_device
    return user_name, device_number
