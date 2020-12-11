from flask_restplus import Namespace, fields


class AccountGroupDto:
    api = Namespace(
        "account/group",
        description="User account group related operations"
    )
    header = api.parser().add_argument("Authorization", location="headers", help="Bearer ")

    add_account_group = api.model(
        "add_account_group",
        {
            "user_groups": fields.List(fields.Nested(api.model("add account group", {
                "name": fields.String(example="<user_1>", description="user name", required=True),
                "display_name": fields.String(example="<user_1(NTPC)>", description="user display name", required=True),
                "comment": fields.String(example="write something", description="comment feature")
            })))
        }
    )

    delete_account_group = api.model(
        "delete_account_group",
        {"user_groups": fields.List(fields.String(required=True, description="delete account group", example="1"))})

    join_account_group = api.model(
        "join_account_group",
        {"users": fields.List(fields.String(required=True, description="join account group", example="1"))})

    leave_account_group = api.model(
        "leave_account_group",
        {"users": fields.List(fields.String(required=True, description="leave account group", example="1"))})

    update_account = api.model(
        "update_account_group",
        {
            "user_groups": fields.List(fields.Nested(api.model("update_account.account", {
                "id": fields.String(example="<user_id_1>", description="user id", required=True),
                "name": fields.String(example="<user_1>", description="user name", required=True),
                "display_name": fields.String(example="<user_1(NTPC)>",
                                              description="user display name", required=True),
                "comment": fields.String(example="write something", description="comment feature")
            })))
        }
    )
