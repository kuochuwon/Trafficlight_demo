# HINT when using leave api, usergroups have no destination. so don't need additional parameter

from flask import request
from flask_api import status
from flask_jwt_extended import jwt_required
from flask_restplus import Resource
from werkzeug.exceptions import NotFound

from app.main.dto.account_group import AccountGroupDto
from app.main.service import ret
from app.main.util.common import aaa_verify, api_exception_handler, check_access_authority
from app.main.view.account_group_response import (response_add_groups,
                                                  response_delete_groups,
                                                  response_join_users,
                                                  response_update_groups,
                                                  response_getall_groups,
                                                  response_leave_users)


api = AccountGroupDto.api
_header = AccountGroupDto.header
_add_account_group = AccountGroupDto.add_account_group
_delete_account_group = AccountGroupDto.delete_account_group
_update_account = AccountGroupDto.update_account
_join_account_group = AccountGroupDto.join_account_group
_leave_account_group = AccountGroupDto.leave_account_group

response_status = {status.HTTP_200_OK: ret.get_code_full(ret.RET_OK),
                   status.HTTP_401_UNAUTHORIZED: ret.get_code_full(ret.RET_NO_CUST_ID),
                   status.HTTP_404_NOT_FOUND: ret.get_code_full(ret.RET_NOT_FOUND)}


@api.route("/getall")
class GetAll(Resource):
    @api.doc(responses=response_status)
    @api.expect(_header, validate=True)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def get(self):
        """ give User list """
        cust_id = aaa_verify()
        response = response_getall_groups(cust_id)
        if not response:
            raise NotFound(ret.http_resp(ret.RET_NOT_FOUND))
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK


@api.route("/add")
class Add(Resource):
    @api.expect(_header, _add_account_group,
                validate=True)
    @api.doc(responses=response_status)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def post(self):
        """ add group """
        cust_id = aaa_verify()
        data = request.json
        response = response_add_groups(cust_id, data)
        if not response:
            raise NotFound(ret.http_resp(ret.RET_NOT_FOUND))
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_201_CREATED


@api.route("/delete")
class Delete(Resource):
    @api.expect(_header, _delete_account_group,
                validate=True)
    @api.doc(responses=response_status)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def delete(self):
        """ delete group """
        cust_id = aaa_verify()
        group_id_list = request.json.get("user_groups")

        response_delete_groups(cust_id, group_id_list)
        return ret.http_resp(ret.RET_OK), status.HTTP_200_OK


@api.route("/update")
class Update(Resource):
    @api.doc(responses=response_status)
    @api.expect(_header, _update_account,
                validate=True)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def put(self):
        """ update device """
        cust_id = aaa_verify()
        payload = request.json
        response_update_groups(cust_id, payload)
        return ret.http_resp(ret.RET_OK), status.HTTP_200_OK


@api.route("/<user_group_id>/join")
class Join(Resource):
    @api.doc(responses=response_status)
    @api.expect(_join_account_group,
                validate=True)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def put(self, user_group_id):
        """ join schedule groups """
        cust_id = aaa_verify()
        payload = request.json
        response_join_users(cust_id, user_group_id, payload)
        return ret.http_resp(ret.RET_OK), status.HTTP_200_OK


@api.route("/<user_group_id>/leave")
class Leave(Resource):
    @api.doc(responses=response_status)
    @api.expect(_leave_account_group,
                validate=True)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def put(self, user_group_id):
        """ join schedule groups """
        cust_id = aaa_verify()
        payload = request.json
        response_leave_users(cust_id, user_group_id, payload)
        return ret.http_resp(ret.RET_OK), status.HTTP_200_OK
