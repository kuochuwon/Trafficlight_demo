from flask_restplus import Namespace, fields


class AccountDto:
    api = Namespace(
        "account",
        description="User account related operations"
    )
    header = api.parser().add_argument("Authorization", location="headers", help="Bearer ")
    get_detail_account = api.model(
        "getdetail",
        {"users": fields.List(fields.String(required=True, description="device id to get detail", example=1))})

    add_account = api.model(
        "add",
        {
            "users": fields.List(fields.Nested(api.model("add_account.account", {
                "name": fields.String(example="<user_1>", description="user name", required=True),
                "display_name": fields.String(example="<user_1(NTPC)>", description="user display name", required=True),
                "email": fields.String(example="123@gmail.com", description="user email address"),
                "telephone": fields.String(example="<0212345678>", description="user telephone number"),
                "comment": fields.String(example="write something", description="comment feature"),
                "password": fields.String(example="1234qwer", description="user password", required=True)
            })))
        }
    )

    delete_account = api.model(
        "delete_account",
        {"users": fields.List(fields.String(required=True, description="delete account", example="1"))})

    update_account = api.model(
        "update",
        {
            "users": fields.List(fields.Nested(api.model("update_account.account", {
                "id": fields.String(example="<user_id_1>", description="user id", required=True),
                "name": fields.String(example="<user_1>", description="user name", required=True),
                "display_name": fields.String(example="<user_1(NTPC)>",
                                              description="user display name"),
                "email": fields.String(example="123@gmail.com", description="user email address"),
                "telephone": fields.String(example="<0212345678>",
                                           description="user telephone number"),
                "comment": fields.String(example="write something", description="comment feature"),
                "password": fields.String(example="1234qwer", description="user password")
            })))
        }
    )
