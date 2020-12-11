from flask_restplus import Namespace, fields


class DeviceGroupDto:
    api = Namespace("device/group", description="device groups")
    header = api.parser().add_argument("Authorization", location="headers", help="Bearer ")

    get_detail_group = api.model(
        "getdetail",
        {"device_groups": fields.List(fields.String(required=True,
                                                    description="device group id to get detail", example=1))})

    add_group = api.model(
        "add_group",
        {"device_groups": fields.List(fields.Nested(api.model("device_groups", {
            "name": fields.String(example="台北市松山區", description="name of add group"),
            "display_name": fields.String(example="松山", description="display name of add group")})))})

    join_group = api.model(
        "join_group",
        {"devices": fields.List(fields.String(required=True, description="groups id of join", example=1))})

    join_usergroup = api.model(
        "join_user_group",
        {"user_groups": fields.List(fields.String(required=True, description="groups id of join", example=1))})

    leave_usergroup = api.model(
        "leave_user_group",
        {"user_groups": fields.List(fields.String(required=True, description="groups id of join", example=1))})

    update_group = api.model(
        "update_group",
        {"device_groups": fields.List(fields.Nested(api.model("device_groups", {
            "id": fields.String(example=1, description="id of renamed group"),
            "name": fields.String(example="烏來區", description="new name of renamed group"),
            "display_name": fields.String(example="新北市烏來區", description="new display name of renamed group")
        })))})

    delete_group = api.model(
        "delete_group",
        {"device_groups": fields.List(fields.String(example=1, required=True, description="device groups"))})
