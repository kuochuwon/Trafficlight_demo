from flask import request
from flask_api import status
from flask_jwt_extended import jwt_required
from flask_restplus import Resource

from werkzeug.exceptions import NotFound

from app.main.dto.account import AccountDto
from app.main.service import ret
from app.main.util.common import aaa_verify, api_exception_handler, check_access_authority
from app.main.view.account_response import (response_add, response_delete,
                                            response_get_detail,
                                            response_getall, response_update)


api = AccountDto.api
_header = AccountDto.header
_get_detail_account = AccountDto.get_detail_account
_add_account = AccountDto.add_account
_delete_account = AccountDto.delete_account
_update_account = AccountDto.update_account


response_status = {status.HTTP_200_OK: ret.get_code_full(ret.RET_OK),
                   status.HTTP_401_UNAUTHORIZED: ret.get_code_full(ret.RET_NO_CUST_ID),
                   status.HTTP_404_NOT_FOUND: ret.get_code_full(ret.RET_NOT_FOUND)}


@api.route("/getall")
class GetAll(Resource):
    @api.expect(_header, validate=True)
    @api.doc(responses=response_status)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def get(self):
        """ give User list """
        cust_id = aaa_verify()
        response = response_getall(cust_id)
        if not response:
            raise NotFound(ret.http_resp(ret.RET_NOT_FOUND))
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK


@api.route("/getdetail")
class GetDetail(Resource):
    @api.expect(_header, _get_detail_account,
                validate=True)
    @api.doc(responses=response_status)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def post(self):
        """ give User list """
        cust_id = aaa_verify()
        user_list = request.json.get("users")
        response = response_get_detail(cust_id, user_list)
        if not response:
            raise NotFound(ret.http_resp(ret.RET_NOT_FOUND))
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK


@api.route("/add")
class Add(Resource):
    @api.expect(_header, _add_account,
                validate=True)
    @api.doc(responses=response_status)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def post(self):
        """ add User """
        cust_id = aaa_verify()
        payload = request.json
        response = response_add(cust_id, payload)
        if not response:
            raise NotFound(ret.http_resp(ret.RET_NOT_FOUND))
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK


@api.route("/delete")
class Delete(Resource):
    @api.expect(_header, _delete_account,
                validate=True)
    @api.doc(responses=response_status)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def delete(self):
        """ Delete User """
        cust_id = aaa_verify()
        user_list = request.json.get("users")
        response_delete(cust_id, user_list)
        return ret.http_resp(ret.RET_OK), status.HTTP_200_OK


@api.route("/update")
class Update(Resource):
    @api.expect(_header, _update_account,
                validate=True)
    @api.doc(responses=response_status)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def put(self):
        """ update device """
        cust_id = aaa_verify()
        payload = request.json
        response_update(cust_id, payload)
        return ret.http_resp(ret.RET_OK), status.HTTP_200_OK
