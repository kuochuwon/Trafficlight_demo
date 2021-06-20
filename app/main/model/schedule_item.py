from sqlalchemy.sql import func

from app.main import db
from app.main.model.schedule_group import sdScheduleGroup


class sdScheduleItem(db.Model):
    __tablename__ = "sd42_schedule_items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day = db.Column(db.String(1), comment="Week Day, 0~6")
    create_time = db.Column(db.DateTime, server_default=func.now(), comment="Create time")
    update_time = db.Column(db.DateTime, server_default=func.now(), comment="Update time")
    time = db.Column(db.String(5), comment="Time, SR+0, SS+0, 19:00")
    dimming = db.Column(db.Integer, comment="Dimming")
    schedule_group_id = db.Column(db.Integer, db.ForeignKey(sdScheduleGroup.id), comment="Schedule Group id")
    cust_id = db.Column(db.Integer, db.ForeignKey("sd10_customers.id"), comment="Customer id")

    def __repr__(self):
        return (
            f"<sdScheduleItem id={self.id}/day={self.day}/time={self.time}"
            f"/dimming={self.dimming}/schedule_group_id={self.schedule_group_id}>"
        )

    @staticmethod
    def add(cust_id, schedule_items, schedule_group):
        days_list = list(schedule_items.keys())
        for days in days_list:
            hour_list = list(schedule_items[days].items())
            for hour_dimm in hour_list:
                obj = sdScheduleItem()
                obj.cust_id = cust_id
                obj.day = days
                obj.time = hour_dimm[0]
                obj.dimming = hour_dimm[1]
                obj.schedule_group = schedule_group

    @staticmethod
    def delete(group_id_list):
        sdScheduleItem.query.filter(
            sdScheduleItem.schedule_group_id.in_(group_id_list)).delete(synchronize_session=False)
