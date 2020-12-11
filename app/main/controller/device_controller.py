from flask import request
from flask_api import status
from flask_jwt_extended import jwt_required
from flask_restplus import Resource

from werkzeug.exceptions import NotFound

from app.main.database.device_sql import getall_devicelist_for_geojson
from app.main.dto.device import GetAllDeviceDto
from app.main.service import ret
from app.main.service.device_helper import get_cust_user_device
from app.main.util.geojson_generate import get_geojson_from_sql_results
from app.main.util.common import aaa_verify, api_exception_handler, check_access_authority
from app.main.view.device_response import (response_add_device,
                                           response_delete_devices,
                                           response_get_detail,
                                           response_update_device)
from app.main.util.redis_handler import (redis_general_add, redis_general_get)


api = GetAllDeviceDto.api
_header = GetAllDeviceDto.header
_get_all_device = GetAllDeviceDto.get_all_device
_add_device = GetAllDeviceDto.add_device
_delete_device = GetAllDeviceDto.delete_device
_update_device = GetAllDeviceDto.update_device
_get_detail_device = GetAllDeviceDto.get_detail_device


response_status = {status.HTTP_200_OK: ret.get_code_full(ret.RET_OK),
                   status.HTTP_401_UNAUTHORIZED: ret.get_code_full(ret.RET_NO_CUST_ID),
                   status.HTTP_404_NOT_FOUND: ret.get_code_full(ret.RET_NOT_FOUND)}


@api.route("/getall")
class GetAll(Resource):
    @api.expect(_header, _get_all_device,
                validate=True)
    @api.doc(responses=response_status)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def post(self):
        """ give User device list """
        cust_id = aaa_verify()
        payload = request.json
        user_name, device_number = get_cust_user_device(payload)

        # print(help('modules'))

        # using redis to enhance efficiency
        namespace = f"traffic_light:device:getall:{cust_id}"
        cache = redis_general_get(namespace)
        if not cache:
            data = getall_devicelist_for_geojson(cust_id,
                                                 user_name,
                                                 device_number)
            response = get_geojson_from_sql_results(data)
            redis_general_add(namespace, response)
        else:
            response = cache

        if not response:
            raise NotFound(ret.http_resp(ret.RET_NOT_FOUND))
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK


@api.route("/add")
class Add(Resource):
    @api.expect(_header, _add_device,
                validate=True)
    @api.doc(responses=response_status)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def post(self):
        """ add device """
        cust_id = aaa_verify()
        payload = request.json
        response = response_add_device(cust_id, payload)
        if not response:
            raise NotFound(ret.http_resp(ret.RET_NOT_FOUND))
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK


@api.route("/delete")
class Delete(Resource):
    @api.expect(_header, _delete_device,
                validate=True)
    @api.doc(responses=response_status)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def delete(self):
        """ delete device """
        cust_id = aaa_verify()
        response_delete_devices(cust_id, request.json.get("devices"))
        return ret.http_resp(ret.RET_OK), status.HTTP_200_OK


@api.route("/update")
class Update(Resource):
    @api.expect(_header, _update_device,
                validate=True)
    @api.doc(responses=response_status)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def put(self):
        """ update device """
        cust_id = aaa_verify()
        payload = request.json
        response_update_device(cust_id, payload)
        return ret.http_resp(ret.RET_OK), status.HTTP_200_OK


@api.route("/getdetail")
class GetDetail(Resource):
    @api.expect(_header, _get_detail_device,
                validate=True)
    @api.doc(responses=response_status)
    @jwt_required
    @check_access_authority
    @api_exception_handler
    def post(self):
        """ get detail device """
        cust_id = aaa_verify()
        device_list = request.json.get("devices")
        response = response_get_detail(cust_id, device_list)
        if not response:
            raise NotFound(ret.http_resp(ret.RET_NOT_FOUND))
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK
