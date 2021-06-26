import os
from datetime import timedelta
from pathlib import Path


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES")))
    WEB_SECRET_KEY = os.getenv("WEB_SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    CORS_ENABLED = True
    #
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": int(os.getenv("DATABASE_POOL_RECYCLE") or "90"),
        "pool_timeout": int(os.getenv("DATABASE_POOL_TIMEOUT") or "900"),
        "pool_size": int(os.getenv("DATABASE_POOL_SIZE") or "10"),
        "max_overflow": int(os.getenv("DATABASE_MAX_OVERFLOW") or "5"),
    }

    REDIS_SERVER = os.getenv("REDIS_SERVER")
    REDIS_PORT = os.getenv("REDIS_PORT")

    #
    LOG_FILE = os.getenv("LOG_FILE") or "log/server.log"
    path = Path(os.path.dirname(LOG_FILE))
    if not (path.exists() and path.is_dir()):
        os.makedirs(path)


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    Config.SQLALCHEMY_ENGINE_OPTIONS["echo"] = False
    Config.SQLALCHEMY_ENGINE_OPTIONS["echo_pool"] = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    Config.SQLALCHEMY_ENGINE_OPTIONS["echo"] = False
    Config.SQLALCHEMY_ENGINE_OPTIONS["echo_pool"] = False


class HerokuConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("HEROKU_DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    Config.SQLALCHEMY_ENGINE_OPTIONS["echo"] = False
    Config.SQLALCHEMY_ENGINE_OPTIONS["echo_pool"] = False


__config_list = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
    heroku=HerokuConfig
)


def get_config(config_name):
    return __config_list.get(config_name, DevelopmentConfig)


jwt_key = Config.JWT_SECRET_KEY


# MQTT Setting
class MQTTConfig:
    CLIENT_ID = str(os.getenv("MQTT_CLIENT_ID"))
    ALIVE = int(os.getenv("MQTT_ALIVE"))
    SERVER = str(os.getenv("MQTT_SERVER"))
    PORT = int(os.getenv("MQTT_PORT"))
    PUBLISH_TOPIC = str(os.getenv("MQTT_PUBLISH_TOPIC"))
    QOS = int(os.getenv("MQTT_QOS"))
