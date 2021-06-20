from sqlalchemy.sql import func

from app.main import db
from app.main.model.device_model import sdDeviceModel
from app.main.model.customer import sdCustomer


class sdLed(db.Model):
    __tablename__ = "sd32_leds"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), comment="Name")
    display_name = db.Column(db.String(50), comment="Display name")
    comment = db.Column(db.Text, comment="Comment")
    create_time = db.Column(db.DateTime, server_default=func.now(), comment="Create time")
    update_time = db.Column(db.DateTime, server_default=func.now(), comment="Update time")
    cust_id = db.Column(db.Integer, db.ForeignKey(sdCustomer.id), comment="Customer id")
    status = db.Column(db.Integer, server_default="0", comment="Device status flag. bit 0: warning, bit 1: error")
    model_id = db.Column(db.Integer, db.ForeignKey(sdDeviceModel.id),
                         server_default="0", comment="Traffic Light model/part no")
    serial_no = db.Column(db.String(50), nullable=False, comment="Serial No")
    device = db.relationship("sdDevice", uselist=False, backref="led")

    __table_args__ = (
        db.UniqueConstraint("serial_no"),
        db.UniqueConstraint("cust_id", "name")
    )

    def __repr__(self):
        return f"<sdLed id={self.id}/name={self.name}/display_name={self.display_name}/sn={self.serial_no}>"

    @staticmethod
    def add(cust_id, led):
        model = db.session.query(sdDeviceModel) \
            .filter(sdDeviceModel.name == led.get("model_name")).first()
        obj = sdLed()
        obj.cust_id = cust_id
        obj.name = led.get("name")
        obj.display_name = led.get("display_name")
        obj.comment = led.get("comment")
        obj.model = model
        obj.serial_no = led.get("serial_no")
        return obj

    @staticmethod
    def update(cust_id, led):
        model = db.session.query(sdDeviceModel) \
            .filter(sdDeviceModel.name == led.get("model_name")).first()
        sdn = led["serial_no"]
        obj = db.session.query(sdLed).filter(sdLed.serial_no == sdn).first()
        if obj:
            obj.cust_id = cust_id
            obj.name = led.get("name")
            obj.display_name = led.get("display_name")
            obj.comment = led.get("comment")
            obj.model = model
            obj.serial_no = led.get("serial_no")
        else:
            obj = sdLed.add(cust_id, led)
        return obj
