from app.main import db
from app.main.model.device import sdDevice
from app.main.model.controller import sdController
from app.main.model.led import sdLed
from app.main.model.device_group import sdDeviceGroup
from app.main.model.user import sdUser
from app.main.model.user_group import sdUserGroup
from app.main.model.schedule_group import sdScheduleGroup


status = ["duplicate"]
str_name = "name"
str_serial = "serial_no"
model_dict = {"devices": sdDevice,
              "controller": sdController,
              "led": sdLed,
              "device_groups": sdDeviceGroup,
              "users": sdUser,
              "user_groups": sdUserGroup,
              "schedule_groups": sdScheduleGroup
              }


def get_query(sdModel, cust_id, string, value, id=None):
    if id is None:
        query = db.session.query(sdModel).filter(getattr(sdModel, "cust_id") == cust_id,
                                                 getattr(sdModel, string) == value).first()
    else:
        query = db.session.query(sdModel).filter(getattr(sdModel, "cust_id") == cust_id,
                                                 getattr(sdModel, string) == value,
                                                 getattr(sdModel, "id") != id).first()
    return query


def device_get_query(sdModel, cust_id, string, value, component_id=None):
    if string == str_serial:
        component_id = db.session.query(sdModel.id).filter(getattr(sdModel, "cust_id") == cust_id,
                                                           getattr(sdModel, string) == value).first()

        query = db.session.query(sdModel).filter(getattr(sdModel, "cust_id") == cust_id,
                                                 getattr(sdModel, string) == value,
                                                 getattr(sdModel, "id") != component_id).first()

        return component_id, query
    else:
        query = db.session.query(sdModel).filter(getattr(sdModel, "cust_id") == cust_id,
                                                 getattr(sdModel, string) == value,
                                                 getattr(sdModel, "id") != component_id).first()

        return query


def checker(model, sdModel, iter_container, cust_id):
    response = {model: []}
    for id, name in iter_container:
        name_query = get_query(sdModel, cust_id, str_name, name, id)
        obj = dict(id=id, name=name, description={})
        if name_query:
            obj["description"] = {"name": status[0]}
        response[model].append(obj)
    return response


def device_checker(model, sdModel, iter_container, cust_id):
    response = {model: []}
    for id, name, ctrl, led in iter_container:
        desc = {}
        name_query = get_query(sdModel, cust_id, str_name, name, id)
        obj = dict(id=id, name=name, controller={}, led={}, description={})
        if name_query:
            obj["description"] = {"name": status[0]}

        if ctrl:
            checked_dict = device_processer(ctrl, sdController, cust_id, obj, "controller")
            obj["controller"].update({"name": ctrl.get("name"), "serial_no": ctrl.get("serial_no")})
            desc.update(checked_dict)

        if led:
            checked_dict = device_processer(led, sdLed, cust_id, obj, "led")
            obj["led"].update({"name": led.get("name"), "serial_no": led.get("serial_no")})
            desc.update(checked_dict)

        obj["description"].update(desc)
        response[model].append(obj)

    return response


def device_processer(oridev, sdModel, cust_id, resp, key):
    the_id, serial_query = device_get_query(sdModel, cust_id, str_serial, oridev.get(str_serial))
    name_query = device_get_query(sdModel, cust_id, str_name,  oridev.get(str_name), the_id)
    checked_dict = {}
    if name_query:
        checked_dict.update({f"{key}.{str_name}": status[0]})
    if serial_query:
        checked_dict.update({f"{key}.{str_serial}": status[0]})

    return checked_dict


def check_db_exist(model, data, cust_id):
    iter_container = []
    sdModel = model_dict[model]

    if model == "devices":
        for id_names in data.get(model):
            ctrl_obj = id_names.get("controller")
            led_obj = id_names.get("led")
            iter_container.append((id_names.get("id"), id_names.get("name"), ctrl_obj, led_obj))
        response = device_checker(model, sdModel, iter_container, cust_id)

    else:
        for id_names in data.get(model):
            iter_container.append((id_names.get("id"), id_names.get("name")))
        response = checker(model, sdModel, iter_container, cust_id)
    return response
