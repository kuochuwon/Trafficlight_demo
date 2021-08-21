from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from .config import get_config, Config
from .log import logger, get_handler

db = SQLAlchemy()
bcrypt = Bcrypt()

jwt = JWTManager()


def create_app(config_name):
    logname = Config.LOG_FILE
    logger.addHandler(get_handler(logname))
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    return app
