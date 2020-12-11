"""
variable "group" in func getall, compose of id, name and display name
rel_dg_ug is a intermediate table for connecting relationships of device groups and user groups
rel_u_ug is a intermediate table for connecting relationships of users and user groups
"""
from sqlalchemy.sql import func

from app.main import db
from app.main.model.user import sdUser
from app.main.model.status_privilege import sdStatusPrivilege

rel_dg_ug = db.Table(
    'sd15_rel_dg_ug',
    db.Column('device_group_id', db.Integer, db.ForeignKey('sd22_device_groups.id')),
    db.Column('user_group_id', db.Integer, db.ForeignKey('sd13_user_groups.id')))

rel_u_ug = db.Table(
    'sd14_rel_u_ug',
    db.Column('user_id', db.Integer, db.ForeignKey('sd11_users.id')),
    db.Column('user_group_id', db.Integer, db.ForeignKey('sd13_user_groups.id')))

rel_role_ug = db.Table(
    'sd16_rel_role_ug',
    db.Column('role_id', db.Integer, db.ForeignKey('sd18_roles.id')),
    db.Column('user_group_id', db.Integer, db.ForeignKey('sd13_user_groups.id')))


class sdUserGroup(db.Model):
    __tablename__ = "sd13_user_groups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), comment="Name", nullable=False)
    display_name = db.Column(db.String(50), comment="Display name")
    comment = db.Column(db.Text, comment="Comment")
    create_time = db.Column(db.DateTime, server_default=func.now(), comment="Create time")
    update_time = db.Column(db.DateTime, server_default=func.now(), comment="Update time")
    cust_id = db.Column(db.Integer, db.ForeignKey("sd10_customers.id"), comment="Customer id")

    rel_dg_ug = db.relationship('sdDeviceGroup', secondary=rel_dg_ug, backref='user_groups')
    rel_u_ug = db.relationship('sdUser', secondary=rel_u_ug, backref='user_groups')
    rel_role_ug = db.relationship('sdRole', secondary=rel_role_ug, backref='user_groups')

    __table_args__ = (db.UniqueConstraint("cust_id", "name"),)

    def __repr__(self):
        return f"<sdUserGroup id={self.id}/name={self.name}/display_name={self.display_name}/cust_id={self.cust_id}"

    @staticmethod
    def getall(cust_id):
        usergroups = db.session.query(sdUserGroup).filter(sdUserGroup.cust_id == cust_id).all()
        return usergroups

    @staticmethod
    def add(cust_id, name, display_name, comment):
        obj = sdUserGroup()
        obj.cust_id = cust_id
        obj.name = name
        obj.display_name = display_name
        obj.comment = comment
        return obj

    # delete_all_users: delete all users, device groups record corresponding to the user group from m2m table
    @staticmethod
    def delete_all_users(cust_id, user_list):
        user_groups = db.session.query(sdUserGroup).filter(sdUserGroup.cust_id == cust_id,
                                                           sdUserGroup.id.in_(user_list)).all()
        # TAG clear() attribute is active only without lazy = dynamic
        for user_group in user_groups:
            dg_rels = user_group.rel_dg_ug
            dg_rels.clear()
            u_rels = user_group.rel_u_ug
            u_rels.clear()
            role_rels = user_group.rel_role_ug
            role_rels.clear()

    @staticmethod
    def delete(cust_id, user_list):
        sdUserGroup.query.filter(sdUserGroup.cust_id == cust_id,
                                 sdUserGroup.id.in_(user_list)).delete(synchronize_session=False)

    @staticmethod
    def update(cust_id, group_id, new_name, new_display_name, new_comment):
        obj = db.session.query(sdUserGroup).filter(sdUserGroup.cust_id == cust_id, sdUserGroup.id == group_id).first()
        obj.name = new_name
        obj.display_name = new_display_name
        obj.comment = new_comment
        return obj

    # user join user group
    @staticmethod
    def join_users(cust_id, user_group_id, user_list):
        selected_user_group = db.session.query(sdUserGroup).filter(
            sdUserGroup.id == user_group_id, sdUserGroup.cust_id == cust_id).first()
        query_obj = db.session.query(sdUser).filter(sdUser.id.in_(user_list), sdUser.cust_id == cust_id).all()
        selected_user_group.rel_u_ug.extend(query_obj)

    # user leave user group
    @staticmethod
    def leave_users(user_group_id, user_list):
        db.session.query(rel_u_ug).filter(rel_u_ug.c.user_group_id == user_group_id).\
            filter(rel_u_ug.c.user_id.in_(user_list)).\
            delete(synchronize_session=False)

    @staticmethod
    def get_status_privilege(usergroup_obj, cust_id, flag, priv_set):
        # status_privilege = []
        for ug_obj in usergroup_obj:
            # get roles of user group
            role_ug = ug_obj.rel_role_ug
            for role in role_ug:
                # get status privilege of role, filter cust_id
                status_privilege = sdStatusPrivilege.get_privilege(role.id, cust_id)
                if flag == 2:
                    for priv_obj in status_privilege:
                        # get status tuple
                        priv_set.add(priv_obj.status_to)
                else:
                    for priv_obj in status_privilege:
                        # get status tuple
                        priv_set.add((str(priv_obj.status_from), str(priv_obj.status_to)))

        return priv_set

    @staticmethod
    def give_user_id_get_roles(user_id):
        user_obj = db.session.query(sdUser).filter(sdUser.id == user_id).first()
        # get user groups of users
        usergroup_obj = user_obj.user_groups
        role_set = set()

        # Gathering data from models using relationship
        for ug_obj in usergroup_obj:
            # get roles of user group
            role_ug = ug_obj.rel_role_ug
            for role in role_ug:
                # get privilege of role
                role_set.add(role.id)
        return role_set

    @staticmethod
    def give_user_id_get_auths(user_id, flag, cust_id=None):
        user_obj = db.session.query(sdUser).filter(sdUser.id == user_id).first()
        # get user groups of users
        usergroup_obj = user_obj.user_groups
        priv_set = set()

        # Gathering data from models using relationship
        if flag == 0:
            for ug_obj in usergroup_obj:
                # get roles of user group
                role_ug = ug_obj.rel_role_ug
                for role in role_ug:
                    # get privilege of role
                    priv = role.privileges
                    for route in priv:
                        # get api route
                        priv_set.add(route.api_route)
        else:
            priv_set = sdUserGroup.get_status_privilege(usergroup_obj, cust_id, flag, priv_set)
        return priv_set
