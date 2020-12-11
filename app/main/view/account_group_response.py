from app.main import db
from app.main.log import logger
from app.main.model.user_group import sdUserGroup
from app.main.util.common import convert_null_emptystr


def response_getall_groups(cust_id):
    try:
        usergroups = sdUserGroup.getall(cust_id)
        if not usergroups:
            return None
        response_users = []
        for usergroup in usergroups:
            users = []
            if usergroup.rel_u_ug:
                userobj = usergroup.rel_u_ug
                for user in userobj:
                    # TAG str changed
                    users.append(str(user.id))
            response_users.append({"id": str(usergroup.id),
                                   "name": usergroup.name,
                                   "display_name": usergroup.display_name,
                                   "users": users})
        response_body = {"user_groups": response_users}
        convert_null_emptystr(response_body)
        logger.debug("success for generate user list.")
        return response_body
    except Exception as e:
        logger.error(f"failed to update data from SQL: {str(e)}")
        raise

    finally:
        db.session.close()


def response_add_groups(cust_id, payload):
    try:
        response_users = []
        usergroup_inputs = payload["user_groups"]
        for usergroup_input in usergroup_inputs:
            obj = sdUserGroup.add(cust_id, usergroup_input.get("name"),
                                  usergroup_input.get("display_name"),
                                  usergroup_input.get("comment"))
            db.session.add(obj)
            db.session.flush()
            # TAG change str here
            response_users.append(dict(id=str(obj.id), name=obj.name))

        db.session.commit()
        response_body = {"users": response_users}
        return response_body
    except Exception as e:
        logger.error(f"failed to add data from SQL: {str(e)}")
        db.session.rollback()
        raise

    finally:
        db.session.close()


def response_delete_groups(cust_id, user_group_list):
    try:
        sdUserGroup.delete_all_users(cust_id, user_group_list)
        sdUserGroup.delete(cust_id, user_group_list)
        db.session.commit()
    except Exception as e:
        logger.error(f"failed to delete data from SQL: {str(e)}")
        db.session.rollback()
        raise

    finally:
        db.session.close()


def response_update_groups(cust_id, payload):
    try:
        user_inputs = payload["user_groups"]
        for user_input in user_inputs:
            obj = sdUserGroup.update(cust_id,
                                     user_input.get("id"),
                                     user_input.get("name"),
                                     user_input.get("display_name"),
                                     user_input.get("comment"))
            db.session.add(obj)
        db.session.commit()
    except Exception as e:
        logger.error(f"failed to update data from SQL: {str(e)}")
        db.session.rollback()
        raise

    finally:
        db.session.close()


def response_join_users(cust_id, user_group_id, payload):
    try:
        user_list = payload["users"]
        sdUserGroup.join_users(cust_id, user_group_id, user_list)
        db.session.commit()
    except Exception as e:
        logger.error(f"failed to join users: {str(e)}")
        db.session.rollback()
        raise
    finally:
        db.session.close()


def response_leave_users(cust_id, user_group_id, payload):
    try:
        user_list = payload["users"]
        sdUserGroup.leave_users(user_group_id, user_list)
        db.session.commit()
    except Exception as e:
        logger.error(f"failed to join users: {str(e)}")
        db.session.rollback()
        raise
    finally:
        db.session.close()
