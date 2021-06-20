from sqlalchemy.sql import func

from app.main import db
from app.main.constant import Constant
from app.main.model.command import sdCommand
from app.main.model.device_group import sdDeviceGroup
from app.main.model.device import sdDevice


class sdCommandDevice(db.Model):
    __tablename__ = "sd61_command_device"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    command_id = db.Column(db.Integer, db.ForeignKey(sdCommand.id), comment="Command id")
    device_group_id = db.Column(db.Integer, db.ForeignKey(sdDeviceGroup.id), comment="Device group id")
    device_id = db.Column(db.Integer, db.ForeignKey(sdDevice.id), comment="Device id")
    status_id = db.Column(db.Integer, nullable=False, comment="Command status")
    status_changed_time = db.Column(db.DateTime, server_default=func.now(), comment="Create time")

    def __repr__(self):
        return (
            f"<sdCommandDevice id={self.id}/command_id={self.command_id}/device_group_id={self.device_group_id}"
            f"/device_id={self.device_id}/status_id={self.status_id}/status_changed_time={self.status_changed_time}>"
        )

    @staticmethod
    def add(command_id, device, device_group):
        obj = sdCommandDevice()
        obj.command_id = command_id
        obj.device_group_id = device_group
        obj.device_id = device
        obj.status_id = Constant.COMMAND_STATUS_RECEIVED
        return obj
