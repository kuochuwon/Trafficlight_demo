from sqlalchemy.sql import func

from app.main import db


class sdSchedule(db.Model):
    __tablename__ = "sd42_schedule"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    counting_time = db.Column(db.Integer, comment="紅綠燈從紅燈變為綠燈的等待時間，單位為秒")
    create_time = db.Column(db.DateTime, server_default=func.now(), comment="Create time")
    update_time = db.Column(db.DateTime, server_default=func.now(), comment="Update time")
    cust_id = db.Column(db.Integer, db.ForeignKey("sd10_customers.id"), comment="Customer id")

    def __repr__(self):
        return (
            f"<sdSchedule id={self.id}"
        )

    @staticmethod
    def add(cust_id, schedule_items, schedule_group):
        days_list = list(schedule_items.keys())
        for days in days_list:
            hour_list = list(schedule_items[days].items())
            for hour_dimm in hour_list:
                obj = sdSchedule()
                obj.cust_id = cust_id
                obj.day = days
                obj.time = hour_dimm[0]
                obj.dimming = hour_dimm[1]
                obj.schedule_group = schedule_group

    @staticmethod
    def delete(group_id_list):
        sdScheduleItem.query.filter(
            sdScheduleItem.schedule_group_id.in_(group_id_list)).delete(synchronize_session=False)
