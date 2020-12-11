from flask_restplus import Namespace, fields


class AuthDto:
    api = Namespace("auth",
                    description="Authentication related operations")
    user_auth = api.model("auth", {
        "custname": fields.String(required=True,
                                  description="Customer name"),
        "username": fields.String(required=True,
                                  description="User name"),
        "password": fields.String(required=True,
                                  description="User password")})

    parser_logout = api.parser()
    parser_logout.add_argument("Authorization", location="headers")

    refresh = api.parser()
    refresh.add_argument("Authorization", location="headers")
