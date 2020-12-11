from flask_restplus import Namespace, fields


class GetAllDeviceDto:
    api = Namespace(
        "device",
        description="User device related operations"
    )
    header = api.parser().add_argument("Authorization", location="headers", help="Bearer ")
    get_all_device = api.model(
        "get_all_device",
        {
            "user": fields.String(required=True, description="User name"),
            "max_device": fields.Integer(
                required=False,
                description="numbers of device returned, ignore = default. 10, 0 = all"
            )
        }
    )

    add_device = api.model(
        "add_device",
        {
            "devices": fields.List(fields.Nested(api.model("add_device.devices", {
                "name": fields.String(example="<name_1>", description="device name"),
                "display_name": fields.String(example="<display_name_1>", description="device display name"),
                "comment": fields.String(example="write something", description="comment feature"),
                "wgs_x": fields.Float(example=27.0, description="device x"),
                "wgs_y": fields.Float(example=29.0, description="device y"),
                "address": fields.String(example="device address", description="device address"),
                "controller": fields.Nested(api.model("add_device.controller", {
                    "model_name": fields.String(example="GPD002-000GT", description="controller model name"),
                    "name": fields.String(example="controller name", description="controller name"),
                    "display_name": fields.String(example="controller dislay name", description="controller dislay name"),
                    "comment": fields.String(example="controller comment", description="controller comment"),
                    "serial_no": fields.String(example="BX0000", description="controller serial number")})),
                "led": fields.Nested(api.model("add_device.led", {
                    "model_name": fields.String(example="LM1109-I1FGT", description="led model name"),
                    "name": fields.String(example="led name", description="led name"),
                    "display_name": fields.String(example="led dislay name", description="led dislay name"),
                    "comment": fields.String(example="led comment", description="led comment"),
                    "serial_no": fields.String(example="BX0000", description="led serial number")}))
            })))
        }
    )
    delete_device = api.model(
        "delete_device",
        {"devices": fields.List(fields.String(example=1, required=True, description="device groups"))})

    update_device = api.model(
        "update_device",
        {
            "devices": fields.List(fields.Nested(api.model("update_device.devices", {
                "id": fields.String(example="<id_1>", description="device id"),
                "name": fields.String(example="<name_1>", description="device name"),
                "display_name": fields.String(example="<display_name_1>", description="device display name"),
                "comment": fields.String(example="write something", description="comment feature"),
                "wgs_x": fields.Float(example=27.0, description="device x"),
                "wgs_y": fields.Float(example=29.0, description="device y"),
                "address": fields.String(example="device address", description="device address"),
                "controller": fields.Nested(api.model("add_device.controller", {
                    "model_name": fields.String(example="GPD002-000GT", description="controller model name"),
                    "name": fields.String(example="controller name", description="controller name"),
                    "display_name": fields.String(example="controller dislay name", description="controller dislay name"),
                    "comment": fields.String(example="controller comment", description="controller comment"),
                    "serial_no": fields.String(example="BX0000", description="controller serial number")})),
                "led": fields.Nested(api.model("add_device.led", {
                    "model_name": fields.String(example="LM1109-I1FGT", description="led model name"),
                    "name": fields.String(example="led name", description="led name"),
                    "display_name": fields.String(example="led dislay name", description="led dislay name"),
                    "comment": fields.String(example="led comment", description="led comment"),
                    "serial_no": fields.String(example="BX0000", description="led serial number")}))
            })))
        }
    )
    get_detail_device = api.model(
        "getdetail",
        {"devices": fields.List(fields.String(required=True, description="device id to get detail", example=1))})
