import json
import redis

from app.main.config import Config
from app.main.log import logger
from app.main.constant import Constant

__redis_pool = redis.ConnectionPool(host=Config.REDIS_SERVER, port=Config.REDIS_PORT,
                                    password='0e6dbc5f3f2aa6aeca6aac1146895061', decode_responses=True)
__redis = redis.Redis(connection_pool=__redis_pool)
__redis_expire = Constant.REDIS_EXPIRE_TIMES


def get_redis_connect():
    with __redis.pipeline(transaction=False) as p:
        return p


# Easy add single key value into redis
def redis_general_add(namespace, data, p=None):
    try:
        if not p:
            p = get_redis_connect()
        p.set(namespace, json.dumps(data))
        p.execute()
        logger.debug(f"Redis new key was set: {namespace}")
    except Exception as e:
        logger.error(f"Redis new key set error: {str(e)}")


def redis_general_get(namespace, p=None):
    try:
        if not p:
            p = get_redis_connect()
        p.get(namespace)
        request_json = p.execute()[0]
        logger.debug(f"Redis key got: {namespace}")
        if not request_json:
            return None
        request_json = json.loads(request_json)
        return request_json
    except Exception as e:
        logger.error(f"Redis process error: {str(e)}")


# Easy delete key
def delete_key_in_redis(namespace, p=None):
    try:
        if not p:
            p = get_redis_connect()

        p.delete(namespace)
        p.execute()
        logger.debug(f"Redis delete key: {namespace}")
    except Exception as e:
        logger.error(f"Redis delete key error: {str(e)}")


def get_multiple_keys(namespace, p=None):
    try:
        if not p:
            p = get_redis_connect()
        p.keys(pattern=f"{namespace}:*")
        multi_keys = p.execute()[0]
        return multi_keys
    except Exception as e:
        logger.error(f"Redis process error: {str(e)}")


def get_multiple_value(key_list, p=None):
    try:
        if not p:
            p = get_redis_connect()
        p.mget(key_list)
        request_json = p.execute()[0]
        return request_json
    except Exception as e:
        logger.error(f"Redis process error: {str(e)}")
