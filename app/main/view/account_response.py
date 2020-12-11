from app.main.log import logger
from app.main.model.user import sdUser
from app.main import db
from app.main.util.common import convert_null_emptystr


def response_getall(cust_id):
    try:
        users = sdUser.getall(cust_id)
        if not users:
            return None
        response_users = []
        # TAG str changed in for loop
        for user in users:
            ugobj = user.user_groups
            involved_ug = [str(ug.id) for ug in ugobj]
            response_users.append(dict(id=str(user.id),
                                       name=user.name,
                                       display_name=user.display_name,
                                       group=involved_ug))
        response_body = {"users": response_users}
        convert_null_emptystr(response_body)
        logger.debug("success for generate user list.")
        return response_body
    except Exception as e:
        logger.error(f"failed to update data from SQL: {str(e)}")
        raise

    finally:
        db.session.close()


def response_get_detail(cust_id, user_list):
    try:
        users = sdUser.getdetail(cust_id, user_list)
        if not users:
            return None
        response_users = []
        for user in users:
            ugobj = user.user_groups
            involved_ug = [str(ug.id) for ug in ugobj]
            response_users.append(dict(id=str(user.id),
                                       name=user.name,
                                       display_name=user.display_name,
                                       group=involved_ug,
                                       email=user.email,
                                       telephone=user.telephone,
                                       comment=user.comment))
        response_body = {"users": response_users}
        logger.debug("success for generate user list.")
        convert_null_emptystr(response_body)
        return response_body
    except Exception as e:
        logger.error(f"failed to update data from SQL: {str(e)}")
        db.session.rollback()
        raise

    finally:
        db.session.close()


def response_add(cust_id, payload):
    try:
        response_users = []
        user_inputs = payload["users"]
        for user_input in user_inputs:
            obj = sdUser.add(cust_id, user_input.get("name"),
                             user_input.get("display_name"),
                             user_input.get("password"),
                             user_input.get("email"),
                             user_input.get("telephone"),
                             user_input.get("comment"))
            db.session.add(obj)
            db.session.flush()
            # TAG change str here
            response_users.append(dict(id=str(obj.id), name=obj.name))

        db.session.commit()
        response_body = {"users": response_users}
        return response_body
    except Exception as e:
        logger.error(f"failed to update data from SQL: {str(e)}")
        db.session.rollback()
        raise

    finally:
        db.session.close()


def response_delete(cust_id, user_list):
    try:
        sdUser.delete_all_user_groups(cust_id, user_list)
        sdUser.delete(cust_id, user_list)
        db.session.commit()
    except Exception as e:
        logger.error(f"failed to update data from SQL: {str(e)}")
        db.session.rollback()
        raise

    finally:
        db.session.close()


def response_update(cust_id, payload):
    try:
        user_inputs = payload["users"]
        for user_input in user_inputs:
            obj = sdUser.update(cust_id,
                                user_input.get("id"),
                                user_input.get("name"),
                                user_input.get("display_name"),
                                user_input.get("password"),
                                user_input.get("email"),
                                user_input.get("telephone"),
                                user_input.get("comment"))
            db.session.add(obj)
        db.session.commit()
    except Exception as e:
        logger.error(f"failed to update data from SQL: {str(e)}")
        db.session.rollback()
        raise

    finally:
        db.session.close()
