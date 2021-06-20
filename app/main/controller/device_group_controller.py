from flask import request
from flask_api import status
from flask_jwt_extended import jwt_required
from flask_restplus import Resource

from werkzeug.exceptions import NotFound

from app.main.dto.device_group import DeviceGroupDto
from app.main.service import ret
from app.main.util.common import aaa_verify, api_exception_handler, check_access_authority
from app.main.view.device_group_response import (response_add_groups,
                                                 response_delete_groups,
                                                 response_getall,
                                                 response_getallsummary,
                                                 response_getdetail,
                                                 response_join_groups,
                                                 response_join_usergroups,
                                                 response_leave_usergroups,
                                                 response_update_groups)


api = DeviceGroupDto.api
_header = DeviceGroupDto.header
_get_detail_device_group = DeviceGroupDto.get_detail_group
_add_group = DeviceGroupDto.add_group
_delete_group = DeviceGroupDto.delete_group
_join_group = DeviceGroupDto.join_group
_join_usergroup = DeviceGroupDto.join_usergroup
_leave_usergroup = DeviceGroupDto.leave_usergroup
_update_group = DeviceGroupDto.update_group


response_status = {status.HTTP_200_OK: ret.get_code_full(ret.RET_OK),
                   status.HTTP_401_UNAUTHORIZED: ret.get_code_full(ret.RET_NO_CUST_ID),
                   status.HTTP_404_NOT_FOUND: ret.get_code_full(ret.RET_NOT_FOUND)}


@api.route("/hello")
class Hello(Resource):
    @api.expect(_header, validate=True)
    @api.doc(responses=response_status)
    def get(self):
        """ show device lists """
        response = "Hello world !!"
        if not response:
            raise NotFound(ret.http_resp(ret.RET_NOT_FOUND))

        return response, status.HTTP_200_OK


@api.route("/getall")
class GetAll(Resource):
    @api.expect(_header, validate=True)
    @api.doc(responses=response_status)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def get(self):
        """ show device lists """
        cust_id = aaa_verify()
        response = response_getall(cust_id)
        if not response:
            raise NotFound(ret.http_resp(ret.RET_NOT_FOUND))

        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK


@api.route("/getdetail")
class GetDetail(Resource):
    @api.expect(_header, _get_detail_device_group,
                validate=True)
    @api.doc(responses=response_status)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def post(self):
        """ show device group detail """
        cust_id = aaa_verify()
        data = request.json
        device_groups_list = data.get("device_groups")
        response = response_getdetail(cust_id, device_groups_list)
        if not response:
            raise NotFound(ret.http_resp(ret.RET_NOT_FOUND))

        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK


@api.route("/getallsummary")
class GetAllSummary(Resource):
    @api.expect(_header, validate=True)
    @api.doc(responses=response_status)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def get(self):
        """ get all device groups """
        cust_id = aaa_verify()
        response = response_getallsummary(cust_id)
        if not response:
            raise NotFound(ret.http_resp(ret.RET_NOT_FOUND))

        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK


@api.route("/add")
class AddGroup(Resource):
    @api.expect(_header, _add_group,
                validate=True)
    @api.doc(responses=response_status)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def post(self):
        """ add group """
        cust_id = aaa_verify()
        data = request.json

        add_groups = [(group.get("name"), group.get("display_name")) for group in data.get("device_groups")]
        response = response_add_groups(add_groups, cust_id)

        if not response:
            raise NotFound(ret.http_resp(ret.RET_NOT_FOUND))
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_201_CREATED


@api.route("/delete")
class DeleteGroup(Resource):
    @api.expect(_header, _delete_group,
                validate=True)
    @api.doc(responses=response_status)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def delete(self):
        """ delete group """
        cust_id = aaa_verify()
        group_id_list = request.json.get("device_groups")
        response_delete_groups(cust_id, group_id_list)

        return ret.http_resp(ret.RET_OK), status.HTTP_200_OK


@api.route("/<group_id>/join")
@api.doc(responses=response_status)
class JoinGroup(Resource):
    @api.expect(_header, _join_group,
                validate=True)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def put(self, group_id):
        """put device(s) into selected group """
        cust_id = aaa_verify()
        response_join_groups(cust_id, group_id, request.json.get("devices"))
        return ret.http_resp(ret.RET_OK), status.HTTP_200_OK


@api.route("/<group_id>/join_ug")
@api.doc(responses=response_status)
class JoinUserGroup(Resource):
    @api.expect(_header, _join_usergroup,
                validate=True)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def put(self, group_id):
        """put user groups into selected device group """
        cust_id = aaa_verify()
        response_join_usergroups(cust_id, group_id, request.json.get("user_groups"))
        return ret.http_resp(ret.RET_OK), status.HTTP_200_OK


@api.route("/<group_id>/leave_ug")
@api.doc(responses=response_status)
class LeaveUserGroup(Resource):
    @api.expect(_header, _leave_usergroup,
                validate=True)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def put(self, group_id):
        """remove user groups from selected device group """
        cust_id = aaa_verify()
        response_leave_usergroups(cust_id, group_id, request.json.get("user_groups"))
        return ret.http_resp(ret.RET_OK), status.HTTP_200_OK


@api.route("/update")
@api.doc(responses=response_status)
class UpdateGroup(Resource):
    @api.expect(_header, _update_group,
                validate=True)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def put(self):
        """update the selected groups """
        cust_id = aaa_verify()

        renamed_items = [(rename.get("id"), rename.get("name"), rename.get("display_name"))
                         for rename in request.json.get("device_groups")]
        response_update_groups(cust_id, renamed_items)
        return ret.http_resp(ret.RET_OK), status.HTTP_200_OK
