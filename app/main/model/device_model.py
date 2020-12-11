from sqlalchemy.sql import func

from app.main import db


class sdDeviceModel(db.Model):
    __tablename__ = "sd30_device_models"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), comment="Traffic Light part no")
    display_name = db.Column(db.String(50), comment="Part description + specification")
    comment = db.Column(db.Text, comment="Comment")
    create_time = db.Column(db.DateTime, server_default=func.now(), comment="Create time")
    update_time = db.Column(db.DateTime, server_default=func.now(), comment="Update time")

    controllers = db.relationship("sdController", backref="model")
    leds = db.relationship("sdLed", backref="model")
