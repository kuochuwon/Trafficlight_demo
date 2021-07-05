import json
import functools
from flask import request
from flask_api import status
from flask_jwt_extended import get_jwt_identity

from werkzeug.exceptions import Unauthorized, HTTPException

from app.main import db
from app.main.log import logger
from app.main.service import ret
from app.main.model.customer import sdCustomer
from app.main.model.user_group import sdUserGroup
# from app.main.model.issue import sdIssue
from app.main.constant import Constant


def aaa_verify():
    try:
        # Process Token and Authentication Authorization Accounting (AAA)
        cust_id = token_decoder()
        cust = auth_verify(cust_id)

        if not cust:
            raise Unauthorized(ret.http_resp(ret.RET_NO_CUST_ID))

        return cust
    except Exception as e:
        logger.error(str(e))
        raise
    finally:
        db.session.close()


def token_decoder():
    token = get_jwt_identity()
    data = json.loads(token)
    cust_id = data.get("cust_id")
    return cust_id


def user_name_decoder():
    token = get_jwt_identity()
    data = json.loads(token)
    user_name = data.get("user_name")
    user_id = data.get("user_id")
    return user_name, user_id


def auth_verify(cust_id):
    cust = sdCustomer.search(cust_id)
    return cust


def api_exception_handler(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            if isinstance(e, HTTPException):
                logger.exception(e)
                return e.description, e.code

            # UNKNOWN exception
            return ret.http_resp(ret.RET_EXCEPTION, ret_hint=str(e)), status.HTTP_404_NOT_FOUND
    return wrapper


def convert_null_emptystr(device_items):
    if isinstance(device_items, dict):
        for k, v in device_items.items():
            if isinstance(v, type(None)):
                device_items[k] = ""
            else:
                convert_null_emptystr(v)
    elif isinstance(device_items, list):
        for index, oneitem in enumerate(device_items):
            if isinstance(oneitem, type(None)):
                device_items[index] = ""
            else:
                convert_null_emptystr(oneitem)
    elif isinstance(device_items, type(None)):
        device_items = ""


def check_access_authority(f):
    def wrapper(*args, **kargs):
        user_name, user_id = user_name_decoder()
        route = str(request.url_rule).replace("/api/v1/", "")
        accessable_status = sdUserGroup.give_user_id_get_auths(user_id, 0)
        db.session.close()
        if route in accessable_status:
            return f(*args, **kargs)
        else:
            return ret.http_resp(ret.RET_AUTHO_ACCESS_FAIL), status.HTTP_401_UNAUTHORIZED
    return wrapper


# def check_status_authority(f):
#     def wrapper(*args, **kargs):
#         """content of *args
#         :param: ((1,),
#                 [{'id': '1', 'assignee_id': '2', 'description': '狀態轉換', 'plan_time': '2020-02-28'}], 3, '2', 'admin')
#         """

#         user_id, status_to, user_name = args[3], args[2], args[4]
#         cust_id, issue_id = args[0][0], args[1][0].get("id")

#         if user_name != Constant.ADMIN:
#             raise Unauthorized(ret.http_resp(ret.RET_AUTH_NO_USER, f"user_name received: {user_name}"))

#         # need to determine whether current issue is None
#         current_issue = sdIssue.getdetail(cust_id, [issue_id], [Constant.SYSTEM_ADMIN])
#         status_from = str(current_issue[0].status_id)
#         accessable_status = sdUserGroup.give_user_id_get_auths(user_id, 1, cust_id)
#         db.session.close()

#         if (status_from, status_to) in accessable_status:
#             return f(*args, **kargs)
#         else:
#             raise Unauthorized(ret.http_resp(ret.RET_AUTHO_STATUS_FAIL))
#     return wrapper
