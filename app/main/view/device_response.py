from app.main.log import logger
from app.main.model.device import sdDevice
from app.main.model.controller import sdController
from app.main.model.led import sdLed
from app.main.util.geojson_generate import dimming_convert
from app.main.util.conv import datetime_to_iso8601
from app.main import db
from app.main.util.common import convert_null_emptystr


def add_device_handler(cust_id, device):
    # if there is lack of led/controller passing None
    led = device.get("led")
    if led is not None:
        led = sdLed.add(cust_id, device["led"])
    controller = device.get("controller")
    if controller is not None:
        controller = sdController.add(cust_id, device["controller"])

    # it is possible to pass None.
    device_obj = sdDevice.add(cust_id, device, led, controller)
    return device_obj


def update_device_handler(cust_id, device):
    # create data to decide led and controller for update.
    data = {"led": None, "controller": None}
    led = device.get("led")
    if led is not None:
        led = sdLed.update(cust_id, device["led"])
        data['led'] = led
    controller = device.get("controller")
    if controller is not None:
        controller = sdController.update(cust_id, device["controller"])
        data['controller'] = controller

    device_obj = sdDevice.update(cust_id, device, data)
    return device_obj


def response_add_device(cust_id, payload):
    try:
        data = payload["devices"]
        devices = []
        for device in data:
            obj = add_device_handler(cust_id, device)
            db.session.add(obj)
            db.session.flush()
            devices.append(dict(id=str(obj.id), name=obj.name))

        db.session.commit()
        response_body = {"devices": devices}
        return response_body
    except Exception as e:
        logger.error(f"The user input may incorrect, {str(e)}")
        raise


def response_delete_devices(cust_id, device_list):
    try:
        sdDevice.delete(cust_id, device_list)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error(f"The user input may incorrect, {str(e)}")
        raise
    finally:
        db.session.close()


def response_update_device(cust_id, payload):
    try:
        data = payload["devices"]
        for device in data:
            obj = update_device_handler(cust_id, device)
            db.session.add(obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error(f"The user input may incorrect, {str(e)}")
        raise
    finally:
        db.session.close()


def response_get_detail(cust_id, device_list):
    try:
        detail = []
        devices = sdDevice.get_detail(cust_id, device_list)
        for device in devices:
            controller = None
            led = None
            device_group = None
            if device.controller:
                controller = dict(id=str(device.controller.id),
                                  name=device.controller.name,
                                  display_name=device.controller.display_name,
                                  comment=device.controller.comment,
                                  create_time=datetime_to_iso8601(device.controller.create_time),
                                  update_time=datetime_to_iso8601(device.controller.update_time),
                                  model_id=device.controller.model.id,
                                  serial_no=device.controller.serial_no,
                                  model_name=device.controller.model.name,
                                  model_display_name=device.controller.model.display_name)
            if device.led:
                led = dict(id=str(device.led.id),
                           name=device.led.name,
                           display_name=device.led.display_name,
                           comment=device.led.comment,
                           create_time=datetime_to_iso8601(device.led.create_time),
                           update_time=datetime_to_iso8601(device.led.update_time),
                           model_id=device.led.model.id,
                           serial_no=device.led.serial_no,
                           model_name=device.led.model.name,
                           model_display_name=device.led.model.display_name)

            if device.device_group:
                device_group = dict(id=str(device.device_group.id),
                                    name=device.device_group.name,
                                    display_name=device.device_group.display_name,
                                    comment=device.device_group.comment,
                                    create_time=datetime_to_iso8601(device.device_group.create_time),
                                    update_time=datetime_to_iso8601(device.device_group.update_time))
            detail.append(dict(id=str(device.id),
                               name=device.name,
                               display_name=device.display_name,
                               comment=device.comment,
                               status=device.status,
                               power_status=device.power_status,
                               wgs_x=device.wgs_x,
                               wgs_y=device.wgs_y,
                               address=device.address,
                               device_group=device_group,
                               controller=controller,
                               led=led))
        convert_null_emptystr(detail)
        response_body = {"devices": detail}

        return response_body
    except Exception as e:
        db.session.rollback()
        logger.error(f"The user input may incorrect, {str(e)}")
        raise
    finally:
        db.session.close()
