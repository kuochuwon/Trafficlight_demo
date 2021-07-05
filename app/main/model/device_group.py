"""
variable "group" in func getall, compose of id, name and display name
"""
from sqlalchemy.sql import func

from app.main import db
from app.main.model.device import sdDevice
from app.main.model.user_group import sdUserGroup, rel_dg_ug


class sdDeviceGroup(db.Model):
    __tablename__ = "sd22_device_groups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), comment="Name", nullable=False)
    display_name = db.Column(db.String(50), comment="Display name")
    comment = db.Column(db.Text, comment="Comment")
    create_time = db.Column(db.DateTime, server_default=func.now(), comment="Create time")
    update_time = db.Column(db.DateTime, server_default=func.now(), comment="Update time")
    cust_id = db.Column(db.Integer, db.ForeignKey("sd10_customers.id"), comment="Customer id")
    schedule_id = db.Column(db.Integer,  db.ForeignKey("sd42_schedule.id"),
                            comment="Schedule id, null means no schedule")

    devices = db.relationship("sdDevice", backref="device_group", lazy="dynamic")

    __table_args__ = (db.UniqueConstraint("cust_id", "name"),)

    def __repr__(self):
        return f"<sdDeviceGroup id={self.id}/name={self.name}/display_name={self.display_name}/cust_id={self.cust_id}"

    # Get cust's all device groups, and associated user groups, devices
    @staticmethod
    def getall(cust_id):
        device_groups_obj = db.session.query(sdDeviceGroup).filter(sdDeviceGroup.cust_id == cust_id).all()
        return device_groups_obj

    @staticmethod
    def get_detail(cust_id, device_group_list):
        device_groups = db.session.query(sdDeviceGroup).filter(sdDeviceGroup.cust_id == cust_id,
                                                               sdDeviceGroup.id.in_(device_group_list)).all()
        return device_groups

    @staticmethod
    def add(name, display_name, cust_id):
        obj = sdDeviceGroup()
        obj.name = name
        obj.display_name = display_name
        obj.cust_id = cust_id
        return obj

    @staticmethod
    def update(group_id, new_name, new_display_name):
        obj = db.session.query(sdDeviceGroup).filter(sdDeviceGroup.id == group_id).first()
        obj.name = new_name
        obj.display_name = new_display_name
        return obj

    @staticmethod
    def delete(cust_id, group):
        # TAG delete m2m table before deleting device groups
        device_groups = sdDeviceGroup.query.filter(sdDeviceGroup.cust_id == cust_id, sdDeviceGroup.id.in_(group))
        for device_group in device_groups:
            ug_rels = device_group.user_groups
            ug_rels.clear()

        # TAG delete device groups
        device_groups.delete(synchronize_session=False)

    # device join device group
    @staticmethod
    def join(group_id, device_id_list):
        devices = db.session.query(sdDevice).filter(sdDevice.id.in_(device_id_list)).all()
        for device in devices:
            device.device_group_id = group_id
            db.session.add(device)

    # user group join device group
    @staticmethod
    def join_device_group(cust_id, device_group_id, user_group_list):
        selected_device_group = db.session.query(sdDeviceGroup).filter(
            sdDeviceGroup.id == device_group_id, sdDeviceGroup.cust_id == cust_id).first()
        query_obj = db.session.query(sdUserGroup).filter(
            sdUserGroup.id.in_(user_group_list), sdUserGroup.cust_id == cust_id).all()
        selected_device_group.user_groups.extend(query_obj)

    # user group leave device group
    @staticmethod
    def leave_device_group(cust_id, device_group_id, user_group_list):
        db.session.query(rel_dg_ug).filter(rel_dg_ug.c.user_group_id.in_(user_group_list),
                                           rel_dg_ug.c.device_group_id == device_group_id).\
            delete(synchronize_session=False)

    @staticmethod
    def get_device_by_group_id(cust_id, device_groups):
        devices = []
        for group in device_groups:
            obj = db.session.query(sdDeviceGroup).filter(sdDeviceGroup.id == group,
                                                         sdDeviceGroup.cust_id == cust_id).first()
            for device in obj.devices.all():
                devices.append((obj.id, device.id))
        return devices
