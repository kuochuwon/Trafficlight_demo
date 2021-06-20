from flask_api import status

from .ret import (
    http_resp, RET_OK, RET_AUTH_MISSING, RET_AUTH_NO_CUST, RET_AUTH_NO_USER, RET_AUTH_WRONG_PASS,
    RET_EXCEPTION
)
from .blacklist_service import save_to_blacklist
from ..util.conv import str_trim
from ..model.user import sdUser
from ..model.customer import sdCustomer


class Auth:
    @staticmethod
    def login_user(data):
        cust_name = str_trim(data.get("cust"))
        user_name = str_trim(data.get("user"))
        user_pass = str_trim(data.get("pass"))
        if not (cust_name and user_name and user_pass):
            return http_resp(RET_AUTH_MISSING), status.HTTP_400_BAD_REQUEST
        try:
            cust = sdCustomer.query.filter_by(name=cust_name).first()
            if not cust:
                return http_resp(RET_AUTH_NO_CUST, cust_name), status.HTTP_401_UNAUTHORIZED
            user = sdUser.query.filter_by(cust_id=cust.id).filter_by(name=user_name).first()
            if not user:
                return http_resp(RET_AUTH_NO_USER, user_name), status.HTTP_401_UNAUTHORIZED
            if user.check_password(data.get("pass")):
                token_hex = sdUser.encode_user_token(user.cust_id, user.id)
                if token_hex:
                    extra = {
                        "token": token_hex
                    }
                    return http_resp(RET_OK, extra=extra), status.HTTP_200_OK
            else:
                return http_resp(RET_AUTH_WRONG_PASS), status.HTTP_401_UNAUTHORIZED
        except Exception as e:
            return http_resp(RET_EXCEPTION, ret_hint=str(e)), status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def logout_user(auth_header):
        token_hex = None
        if auth_header:
            headers = auth_header.split(" ")
            if headers[0] == "Bearer":
                token_hex = headers[1]
        if token_hex:
            save_to_blacklist(token_hex)
        return http_resp(RET_OK), status.HTTP_200_OK
