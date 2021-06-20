from app.main.model.user import sdUser
from app.main.model.customer import sdCustomer
from app.main.model.blacklist import sdBlacklistToken
from app.main import db
from app.main.log import logger
import json

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity


def decode_token_info():
    token = get_jwt_identity()
    data = json.loads(token)
    return data


def search_cust(cust_name):
    return sdCustomer.search_by_name(cust_name)


def search_user(cust_id, cust_name):
    return sdUser.search(cust_id, cust_name)


def generate_user_tokens(cust_id, user_id, user_name):
    try:
        identity = json.dumps({"cust_id": cust_id, "user_id": user_id, "user_name": user_name})

        tokens = {
            "token": {
                "access_token": create_access_token(identity=identity),
                "refresh_token": create_refresh_token(identity=identity)
            }
        }

        return tokens
    except Exception as e:
        logger.error(f"failed to generate_user_tokens: {str(e)}")
        raise


def logout_user(token):
    try:
        obj = sdBlacklistToken.revoke_token(token)
        db.session.add(obj)
        db.session.commit()
    except Exception as e:
        logger.error(f"failed to update data from SQL: {str(e)}")
        db.session.rollback()
        raise

    finally:
        db.session.close()


def access_token(token):
    data = json.loads(token)
    identity = json.dumps(data)
    token = {
        "access_token": create_access_token(identity=identity)
    }

    return token


def get_user_role(user_id):
    role_dict = {"role": []}
    user = db.session.query(sdUser).filter(sdUser.id == user_id).first()
    usergroups = user.user_groups
    for usergroup in usergroups:
        role_ug = usergroup.rel_role_ug
        for role in role_ug:
            role_dict["role"].append(dict(
                # TAG change str here
                role_id=str(role.id),
                role_name=role.name
            ))
    return role_dict
