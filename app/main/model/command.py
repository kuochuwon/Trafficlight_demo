from sqlalchemy.sql import func
import datetime

from app.main.constant import Constant
from app.main import db


class sdCommand(db.Model):
    __tablename__ = "sd60_command"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.Integer, nullable=False, comment="Command action, 0 = dimming, 1 = power on/off")
    value = db.Column(db.String(5), nullable=False,
                      comment="Command value, dimming = 0~100, power = 0/1 (off/on), schedule = incre (y/n)")
    create_time = db.Column(db.DateTime, server_default=func.now(), comment="Create time")
    schedule_value = db.Column(db.String(200), comment="Save schedule value in json type")
    cust_id = db.Column(db.Integer, db.ForeignKey("sd10_customers.id"), comment="Customer id")

    command_device = db.relationship("sdCommandDevice", backref="command", lazy="dynamic")

    def __repr__(self):
        return f"<sdCommand id={self.id}/action={self.action}/value={self.value}/create_time={self.create_time}"

    @staticmethod
    def add(cust_id, action, value):
        obj = sdCommand()
        obj.action = action
        obj.value = str(value)
        obj.cust_id = cust_id
        return obj

    @staticmethod
    def update_status(command_id):
        obj = db.session.query(sdCommand).filter(sdCommand.id == command_id).first()
        for device in obj.command_device.all():
            device.status_id = Constant.COMMAND_STATUS_QUEUE
            device.status_changed_time = datetime.datetime.now()
