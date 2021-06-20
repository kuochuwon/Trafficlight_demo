from sqlalchemy.sql import func

from app.main import db
from app.main.model.customer import sdCustomer
from app.main.model.device_model import sdDeviceModel


class sdController(db.Model):
    __tablename__ = "sd31_controllers"
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
    device = db.relationship("sdDevice", uselist=False, backref="controller")

    __table_args__ = (
        db.UniqueConstraint("serial_no"),
        db.UniqueConstraint("cust_id", "name")
    )

    def __repr__(self):
        return f"<sdController id={self.id}/name={self.name}/display_name={self.display_name}/sn={self.serial_no}>"

    @staticmethod
    def add(cust_id, controller):
        model = db.session.query(sdDeviceModel)\
            .filter(sdDeviceModel.name == controller.get("model_name")).first()
        obj = sdController()
        obj.cust_id = cust_id
        obj.name = controller.get("name")
        obj.display_name = controller.get("display_name")
        obj.comment = controller.get("comment")
        obj.serial_no = controller.get("serial_no")
        obj.model = model
        return obj

    @staticmethod
    def update(cust_id, controller):
        sdn = controller.get("serial_no")
        model = db.session.query(sdDeviceModel)\
            .filter(sdDeviceModel.name == controller.get("model_name")).first()
        obj = db.session.query(sdController).filter(sdController.serial_no == sdn).first()
        if obj:
            obj.cust_id = cust_id
            obj.name = controller.get("name")
            obj.display_name = controller.get("display_name")
            obj.comment = controller.get("comment")
            obj.serial_no = controller.get("serial_no")
            obj.model = model
        else:
            obj = sdController.add(cust_id, controller)
        return obj
