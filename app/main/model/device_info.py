from sqlalchemy.sql import func

from app.main import db
from app.main.model.customer import sdCustomer
from app.main.model.device import sdDevice


class sdDeviceInfo(db.Model):
    __tablename__ = "sd23_device_infos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, db.ForeignKey(sdDevice.id), comment="Device id")
    comment = db.Column(db.Text, comment="Comment")
    create_time = db.Column(db.DateTime, server_default=func.now(), comment="Create time")
    update_time = db.Column(db.DateTime, server_default=func.now(), comment="Update time")
    cust_id = db.Column(db.Integer, db.ForeignKey(sdCustomer.id), comment="Customer id")
    voltage = db.Column(db.Float, comment="Voltage")
    current = db.Column(db.Float, comment="Current")
    pf = db.Column(db.Float, comment="Power factor")
    power = db.Column(db.Float, comment="Power value")
    temperature = db.Column(db.Float, comment="Temperature")

    __table_args__ = (db.UniqueConstraint("cust_id", "device_id"),)

    def __repr__(self):
        return (
            f"<sdDeviceInfo id={self.id}/device_id={self.device_id}/cust_id={self.cust_id}"
            f"/voltage={self.voltage}/current={self.current}/pf={self.pf}/power={self.power}>"
            f"/temperature={self.temperature}/lumming={self.lumming}"
        )
