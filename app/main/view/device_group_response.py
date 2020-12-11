"""
variable name explanation:

d_in_dg: devices in the device group, data type: list

involved_ug: user groups that device group involved, data type: list
"""

from app.main.log import logger
from app.main.util.conv import datetime_to_iso8601
from app.main.model.device_group import sdDeviceGroup
from app.main.model.device import sdDevice
from app.main.model.customer import sdCustomer
from app.main import db
from app.main.database.device_sql import get_all_summary_table
from app.main.util.common import convert_null_emptystr


def check(cust_id):
    try:
        cust = sdCustomer.search(cust_id)
        return cust
    except Exception as e:
        logger.error(f"failed to update data from SQL: {str(e)}")
        raise
    finally:
        db.session.close()


def response_getall(cust_id):
    try:
        device_groups_obj = sdDeviceGroup.getall(cust_id)
        if not device_groups_obj:
            return None
        response_body = {}
        response_body.update({"device_groups": []})

        d_in_dg = {}
        # TAG str changed in for loop
        for device_group in device_groups_obj:
            d_in_dg[device_group.id] = [str(device.id) for device in device_group.devices]
            ugobj = device_group.user_groups
            involved_ug = [str(ug.id) for ug in ugobj]
            response_body["device_groups"].append({"id": str(device_group.id),
                                                   "name": device_group.name,
                                                   "display_name": device_group.display_name,
                                                   "user_groups": involved_ug,
                                                   "devices": d_in_dg[device_group.id]})
        logger.debug("success for generate device list.")
        convert_null_emptystr(response_body)
        return response_body
    except Exception as e:
        logger.error(f"failed to fetch data from SQL: {str(e)}")
        raise
    finally:
        db.session.close()


def response_getdetail(cust_id, device_groups_list):
    try:
        device_groups_obj = sdDeviceGroup.get_detail(cust_id, device_groups_list)
        if not device_groups_obj:
            return None
        device_groups = []
        for device_group in device_groups_obj:
            schedules_id, schedules_name = "", ""

            if device_group.schedule_group:
                schedules_id = device_group.schedule_group.id
                schedules_name = device_group.schedule_group.name
            device_groups.append({"id": str(device_group.id),
                                  "name": device_group.name,
                                  "display_name": device_group.display_name,
                                  "comment": device_group.comment,
                                  "create_time": datetime_to_iso8601(device_group.create_time),
                                  "update_time": datetime_to_iso8601(device_group.update_time),
                                  "user_groups": [str(user_group.id) for user_group in device_group.user_groups],
                                  "devices": [str(device.id) for device in device_group.devices],
                                  "schedules_id": str(schedules_id),
                                  "schedules_name": schedules_name})

        response_body = {"device_groups": device_groups}
        convert_null_emptystr(response_body)
        return response_body
    except Exception as e:
        logger.error(f"failed to fetch data from SQL: {str(e)}")
        raise


def response_get_dgug_schedule(cust_id):
    dg_ug = dict()
    sched_group = dict()
    all_device_groups = sdDeviceGroup.getall(cust_id)
    for device_group in all_device_groups:
        ug_id_name = [
            dict(id=str(ug.id), name=ug.name) for ug in device_group.user_groups
        ]
        dg_ug.update({device_group.id: ug_id_name})
        if device_group.schedule_group:
            sched = dict(id=str(device_group.schedule_group.id),
                         name=device_group.schedule_group.name)
            sched_group.update({device_group.id: sched})
    return dg_ug, sched_group


def response_getallsummary(cust_id):
    try:
        groups = get_all_summary_table(cust_id)
        if not groups:
            return None
        user_groups, schedule_group = response_get_dgug_schedule(cust_id)
        response_list = []
        for group_id, name, display_name, device_count, poweroff_count, warning_count, error_count in groups:
            # TAG str changed
            response_list.append({"id": str(group_id),
                                  "name": name,
                                  "display_name": display_name,
                                  "user_groups": user_groups.get(group_id),
                                  "schedule_groups": schedule_group.get(group_id),
                                  "device_count": device_count,
                                  "warning_count": warning_count,
                                  "error_count": error_count,
                                  "poweroff_count": poweroff_count})

        response_body = {"device_groups": response_list}
        convert_null_emptystr(response_body)
        logger.debug("success for generate device list.")
        return response_body
    except Exception as e:
        logger.error(f"failed to fetch data from SQL: {str(e)}")
        raise
    finally:
        db.session.close()


def response_add_groups(groups, cust_id):
    try:
        added_groups = []
        for name, display_name in groups:
            obj = sdDeviceGroup.add(name, display_name, cust_id)
            db.session.add(obj)
            db.session.flush()
            # TAG str changed
            added_groups.append(dict(id=str(obj.id), name=obj.name))

        db.session.commit()
        response_body = {}
        response_body.update({"device_groups": added_groups})
        return response_body
    except Exception as e:
        logger.error(f"failed to update data to SQL: {str(e)}")
        db.session.rollback()
        raise
    finally:
        db.session.close()


def response_delete_groups(cust_id, device_groups):
    try:
        #  get device_id for join ungroup
        device_id_list = sdDevice.get_devices_in_groups(cust_id, device_groups)
        if device_id_list:
            sdDeviceGroup.join(None, device_id_list)
        sdDeviceGroup.delete(cust_id, device_groups)
        db.session.commit()
    except Exception as e:
        logger.error(f"failed to update data to SQL: {str(e)}")
        db.session.rollback()
        raise
    finally:
        db.session.close()


def response_join_groups(cust_id, group_id, devices):
    try:
        sdDeviceGroup.join(group_id, devices)
        db.session.commit()
    except Exception as e:
        logger.error(f"failed to join devices: {str(e)}")
        db.session.rollback()
        raise

    finally:
        db.session.close()


def response_join_usergroups(cust_id, device_group_id, user_group_list):
    try:
        sdDeviceGroup.join_device_group(cust_id, device_group_id, user_group_list)
        db.session.commit()
    except Exception as e:
        logger.error(f"failed to join devices: {str(e)}")
        db.session.rollback()
        raise

    finally:
        db.session.close()


def response_leave_usergroups(cust_id, device_group_id, user_group_list):
    try:
        sdDeviceGroup.leave_device_group(cust_id, device_group_id, user_group_list)
        db.session.commit()
    except Exception as e:
        logger.error(f"failed to join users: {str(e)}")
        db.session.rollback()
        raise
    finally:
        db.session.close()


def response_update_groups(cust_id, device_groups):
    try:
        for group_id, new_name, new_display_name in device_groups:
            obj = sdDeviceGroup.update(group_id, new_name, new_display_name)
            db.session.add(obj)

        db.session.commit()

    except Exception as e:
        logger.error(f"failed to update data to SQL: {str(e)}")
        db.session.rollback()
        raise

    finally:
        db.session.close()
