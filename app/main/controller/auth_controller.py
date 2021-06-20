from flask import request
from flask_api import status
from flask_jwt_extended import (get_jwt_identity, get_raw_jwt,
                                jwt_refresh_token_required)
from flask_restplus import Resource

from werkzeug.exceptions import Unauthorized, BadRequest

from app.main import jwt
from app.main.dto.auth import AuthDto
from app.main.model.blacklist import sdBlacklistToken
from app.main.service import ret
from app.main.util.conv import str_trim
from app.main.util.common import api_exception_handler
from app.main.view.auth_response import (access_token, generate_user_tokens,
                                         logout_user, search_cust, search_user,
                                         get_user_role)

api = AuthDto.api
_user_auth = AuthDto.user_auth
_parser_logout = AuthDto.parser_logout
_refresh = AuthDto.refresh


@jwt.expired_token_loader
@api_exception_handler
def expired_token_handler(callback):
    return ret.http_resp(ret.RET_AUTH_TOKEN_EXPIRED), status.HTTP_401_UNAUTHORIZED


@jwt.unauthorized_loader
@api_exception_handler
def missing_header_handler(callback):
    return ret.http_resp(ret.RET_AUTH_TOKEN_MISSING), status.HTTP_401_UNAUTHORIZED


@api.route("/login")
@api.response(status.HTTP_200_OK,
              ret.get_code_full(ret.RET_OK))
@api.response(status.HTTP_400_BAD_REQUEST,
              ret.get_code_full(ret.RET_AUTH_MISSING))
@api.response(status.HTTP_401_UNAUTHORIZED,
              f"{ret.get_code_full(ret.RET_AUTH_NO_CUST)}, {ret.get_code_full(ret.RET_AUTH_NO_USER)}, "
              f"or {ret.get_code_full(ret.RET_AUTH_WRONG_PASS)}")
class UserLogin(Resource):
    @api.doc("User login")
    @api.expect(_user_auth,
                validate=True)
    @api_exception_handler
    def post(self):
        """ User login """
        payload = request.json
        cust_name = str_trim(payload.get("custname"))
        user_name = str_trim(payload.get("username"))
        user_pass = str_trim(payload.get("password"))

        if not (cust_name and user_name and user_pass):
            raise BadRequest(ret.http_resp(ret.RET_AUTH_MISSING))

        cust = search_cust(cust_name)
        if not cust:
            raise Unauthorized(ret.http_resp(ret.RET_AUTH_NO_CUST, cust_name))

        user = search_user(cust.id, user_name)
        if not user:
            raise Unauthorized(ret.http_resp(ret.RET_AUTH_NO_USER, user_name))

        if user.check_password(user_pass):
            resp = generate_user_tokens(str(cust.id), str(user.id), user_name)
            resp.update(get_user_role(user.id))
            if resp:
                return ret.http_resp(ret.RET_OK, extra=resp), status.HTTP_200_OK
        else:
            raise Unauthorized(ret.http_resp(ret.RET_AUTH_WRONG_PASS))


@api.route("/logout")
@api.expect(_parser_logout)
@api.response(status.HTTP_200_OK,
              ret.get_code_full(ret.RET_OK))
@api.response(status.HTTP_401_UNAUTHORIZED,
              f"{ret.get_code_full(ret.RET_AUTH_FAIL)}, {ret.get_code_full(ret.RET_AUTH_TOKEN_EXPIRED)}")
class UserLogout(Resource):
    @api.doc("User logout")
    @jwt_refresh_token_required
    @api_exception_handler
    def get(self):
        jti = get_raw_jwt().get("jti")
        if jti:
            is_in_blacklist = sdBlacklistToken.check_is_in_blacklist(jti)
            if not is_in_blacklist:
                logout_user(jti)
                return ret.http_resp(ret.RET_OK), status.HTTP_200_OK

            else:
                raise Unauthorized(ret.http_resp(ret.RET_AUTH_TOKEN_EXPIRED))
        else:
            raise Unauthorized(ret.http_resp(ret.RET_AUTH_FAIL))


@api.route("/refresh")
@api.expect(_refresh)
@api.response(status.HTTP_200_OK,
              ret.get_code_full(ret.RET_OK))
class Refresh(Resource):
    @api.doc("Get Access")
    @jwt_refresh_token_required
    @api_exception_handler
    def post(self):
        refresh = get_jwt_identity()
        token = access_token(refresh)
        return ret.http_resp(ret.RET_OK, extra=token), status.HTTP_200_OK
