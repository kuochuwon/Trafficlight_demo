from sqlalchemy.sql import func

from app.main import db
from app.main.model.device_group import sdDeviceGroup


class sdScheduleGroup(db.Model):
    __tablename__ = "sd41_schedule_groups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), comment="Name", nullable=False)
    display_name = db.Column(db.String(50), comment="Display name")
    comment = db.Column(db.Text, comment="Comment")
    create_time = db.Column(db.DateTime, server_default=func.now(), comment="Create time")
    update_time = db.Column(db.DateTime, server_default=func.now(), comment="Update time")
    scheme = db.Column(db.String(4), comment="Schedule Time Scheme, 24h and srss")
    incre = db.Column(db.String(1), comment="Increase Light, y/n")
    cust_id = db.Column(db.Integer, db.ForeignKey("sd10_customers.id"), comment="Customer id")

    device_groups = db.relationship("sdDeviceGroup", backref="schedule_group", lazy="dynamic")
    schedule_items = db.relationship("sdScheduleItem", backref="schedule_group", lazy="dynamic")

    __table_args__ = (db.UniqueConstraint("cust_id", "name"),)

    def __repr__(self):
        return (
            f"<sdScheduleGroup id={self.id}/name={self.name}/display_name={self.display_name}"
            f"/scheme={self.scheme}/incre={self.incre}>"
        )

    @staticmethod
    def getall_group(cust_id):
        query = db.session.query(sdScheduleGroup).filter(sdScheduleGroup.cust_id == cust_id).all()
        return query

    @staticmethod
    def add(cust_id, schedule_group):
        obj = sdScheduleGroup()
        obj.cust_id = cust_id
        obj.name = schedule_group.get("name")
        obj.display_name = schedule_group.get("display_name")
        obj.comment = schedule_group.get("comment")
        obj.scheme = schedule_group.get("scheme")
        obj.incre = schedule_group.get("incre")
        return obj

    @staticmethod
    def update(cust_id, schedule):
        obj = db.session.query(sdScheduleGroup).filter(sdScheduleGroup.cust_id == cust_id)\
            .filter(sdScheduleGroup.id == schedule.get("id")).first()
        obj.name = schedule.get("name")
        obj.display_name = schedule.get("display_name")
        obj.comment = schedule.get("comment")
        obj.scheme = schedule.get("scheme")
        obj.incre = schedule.get("incre")

        obj.schedule_items.delete()
        return obj

    @staticmethod
    def get_detail(cust_id, groups):
        query = db.session.query(sdScheduleGroup).filter(sdScheduleGroup.cust_id == cust_id)\
            .filter(sdScheduleGroup.id.in_(groups)).all()
        return query

    @staticmethod
    def delete(group_id_list, cust_id):
        # set device group's schedule id as None
        sdScheduleGroup.join(cust_id, group_id_list, None, "schedule_id")
        sdScheduleGroup.query.filter(sdScheduleGroup.id.in_(group_id_list)).delete(synchronize_session=False)

    @staticmethod
    def join(cust_id, group_id_list, schedule_group_id, column):
        # getattr helps us using this method more flexible (ex: join and delete method)
        device_groups_list = db.session.query(sdDeviceGroup).filter(sdDeviceGroup.cust_id == cust_id)\
            .filter(getattr(sdDeviceGroup, column).in_(group_id_list)).all()
        if device_groups_list:
            # update the schedule_id of device group into selected schedule_group_id
            for device_group in device_groups_list:
                device_group.schedule_id = schedule_group_id
