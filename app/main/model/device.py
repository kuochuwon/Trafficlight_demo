from sqlalchemy.sql import func, or_

from app.main import db
from app.main.model.controller import sdController
from app.main.model.customer import sdCustomer
from app.main.model.led import sdLed


class sdDevice(db.Model):
    __tablename__ = "sd21_devices"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), comment="Name")
    display_name = db.Column(db.String(50), comment="Display name")
    comment = db.Column(db.Text, comment="Comment")
    create_time = db.Column(db.DateTime, server_default=func.now(), comment="Create time")
    update_time = db.Column(db.DateTime, server_default=func.now(), comment="Update time")
    dev_type = db.Column(db.Integer, server_default="0",
                         comment="Device type: 0: unknown, 1: traffic light, 2: others")
    cust_id = db.Column(db.Integer, db.ForeignKey(sdCustomer.id), comment="Customer id")
    vendor_id = db.Column(db.Integer, db.ForeignKey(sdCustomer.id), comment="Vendor id")
    status = db.Column(db.Integer, server_default="0",
                       comment="Device status flag(bit).  0: warning, bit 1: error，可持續新增")
    power_status = db.Column(db.Integer, comment="Device power status. null: unknown, 0: off, 1: on")
    device_group_id = db.Column(db.Integer, db.ForeignKey("sd22_device_groups.id"),
                                comment="Device group id, null means ungroup")
    controller_id = db.Column(db.Integer, db.ForeignKey(sdController.id), comment="Controller id")
    led_id = db.Column(db.Integer, db.ForeignKey(sdLed.id), comment="LED id")
    vender_device_id = db.Column(db.String(25), comment="Vender device id")
    wgs_x = db.Column(db.Float, comment="GPS X")
    wgs_y = db.Column(db.Float, comment="GPS Y")
    address = db.Column(db.String(100), comment="Address")

    device_info = db.relationship("sdDeviceInfo", uselist=False, backref="device")
    __table_args__ = (db.UniqueConstraint("cust_id", "name"),)

    def __repr__(self):
        return (
            f"<sdDevice id={self.id}/name={self.name}/display_name={self.display_name}/cust_id={self.cust_id}"
            f"/wgs_x={self.wgs_x}/wgs_y={self.wgs_y}/address={self.address}>"
            f"/controller_id={self.controller_id}/led_id={self.led_id}"
        )

    @staticmethod
    def delete(cust_id, device_list):
        sdDevice.query.filter(sdDevice.cust_id == cust_id,
                              sdDevice.id.in_(device_list)).delete(synchronize_session=False)

    @staticmethod
    def get_detail(cust_id, device_id_list):
        devices = db.session.query(sdDevice).filter(or_(sdDevice.cust_id == cust_id,
                                                        sdDevice.vendor_id == cust_id),
                                                    sdDevice.id.in_(device_id_list)).all()
        return devices

    @staticmethod
    def get_devices_in_groups(cust_id, group_id_list):

        id_list = []
        device_id_tuple = db.session.query(sdDevice.id).filter(sdDevice.cust_id == cust_id,
                                                               sdDevice.device_group_id.in_(group_id_list)).all()
        for device_id in device_id_tuple:
            id_list.append(device_id[0])
        return id_list

    @staticmethod
    def add(cust_id, device, led, controller):
        obj = sdDevice()
        obj.cust_id = cust_id
        obj.name = device.get("name")
        obj.display_name = device.get("display_name")
        obj.comment = device.get("comment")
        obj.controller = controller
        obj.led = led
        obj.wgs_x = device.get('wgs_x')
        obj.wgs_y = device.get('wgs_y')
        obj.address = device.get('address')
        return obj

    @staticmethod
    def update(cust_id, device, data):

        obj = db.session.query(sdDevice).filter(sdDevice.id == device["id"]).first()
        if obj:
            obj.cust_id = cust_id
            obj.name = device.get("name")
            obj.display_name = device.get("display_name")
            obj.comment = device.get("comment")
            obj.wgs_x = device.get("wgs_x")
            obj.wgs_y = device.get("wgs_y")
            obj.address = device.get("address")

        # if threre is led or controller then update.
        led = data.get("led")
        if led:
            obj.led = led

        controller = data.get("controller")
        if controller:
            obj.controller = controller

        return obj
