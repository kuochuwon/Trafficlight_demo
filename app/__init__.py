from flask_restplus import Api
from flask import Blueprint
from app.main import jwt
from app.main.controller.auth_controller import api as auth_ns
from app.main.controller.device_controller import api as device_ns
from app.main.controller.device_group_controller import api as device_group_ns
from app.main.controller.account_controller import api as account_ns
from app.main.controller.account_group_controller import api as account_group_ns

blueprint = Blueprint("api",
                      __name__,
                      url_prefix="/api/v1")
api = Api(blueprint,
          title="Roy Traffic light system demo",
          version="0.1.0",
          description="Roy Traffic light system demo")

jwt._set_error_handler_callbacks(api)

api.add_namespace(auth_ns,
                  path="/auth")
api.add_namespace(device_ns,
                  path="")
api.add_namespace(device_group_ns,
                  path="")
api.add_namespace(account_ns,
                  path="")
api.add_namespace(account_group_ns,
                  path="")
