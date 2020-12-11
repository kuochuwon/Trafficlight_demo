from sqlalchemy.sql import func

from app.main import db


class sdCustomer(db.Model):
    __tablename__ = "sd10_customers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, nullable=False, index=True, comment="Name")
    display_name = db.Column(db.String(50), nullable=False, comment="Display name")
    comment = db.Column(db.Text, comment="Comment")
    status = db.Column(db.Integer, nullable=False, server_default="0", comment="Status")
    create_time = db.Column(db.DateTime, nullable=False, server_default=func.now(), comment="Create time")
    update_time = db.Column(db.DateTime, nullable=False, server_default=func.now(), comment="Update time")
    cust_id = db.Column(db.Integer, db.ForeignKey("sd10_customers.id"), comment="Vendor of customer")
    issue_namespace = db.Column(db.String(50), nullable=False,
                                server_default="CUSTOM-{datetime:%Y%m%d}-{serial_no:05d}",
                                comment="Issue number namespace")

    vendors = db.relationship("sdCustomer", lazy="dynamic")
    users = db.relationship("sdUser", backref="cust", lazy="dynamic")
    controllers = db.relationship("sdController", backref="cust", lazy="dynamic")
    leds = db.relationship("sdLed", backref="cust", lazy="dynamic")
    device_groups = db.relationship("sdDeviceGroup", backref="cust", lazy="dynamic")
    schedule_groups = db.relationship("sdScheduleGroup", backref="cust", lazy="dynamic")
    schedule_items = db.relationship("sdScheduleItem", backref="cust", lazy="dynamic")
    codes = db.relationship("sdCode", backref="cust", lazy="dynamic")
    user_groups = db.relationship("sdUserGroup", backref="cust", lazy="dynamic")
    serial_number = db.relationship("sdSerialNumber", backref="cust", lazy="dynamic")
    status_privilege = db.relationship("sdStatusPrivilege", backref="cust", lazy="dynamic")
    device_info = db.relationship("sdDeviceInfo", backref="cust", lazy="dynamic")

    cust_devices = db.relationship(
        "sdDevice", foreign_keys="sdDevice.cust_id", backref="cust", lazy="dynamic")
    vendor_devices = db.relationship(
        "sdDevice", foreign_keys="sdDevice.vendor_id", backref="vendor", lazy="dynamic")

    cust_issue = db.relationship(
        "sdIssue", foreign_keys="sdIssue.cust_id", backref="cust", lazy="dynamic")
    vendor_issue = db.relationship(
        "sdIssue", foreign_keys="sdIssue.vendor_id", backref="vendor", lazy="dynamic")

    def __repr__(self):
        return f"<sdCustomer id={self.id}/name={self.name}/display_name={self.display_name}>"

    @staticmethod
    def search(cust_id):
        customer = db.session.query(sdCustomer.id).filter(sdCustomer.id == cust_id).first()
        return customer

    @staticmethod
    def search_by_name(cust_name):
        customer = sdCustomer.query.filter_by(name=cust_name).first()
        return customer

    @staticmethod
    def search_cust(cust_id):
        customer = db.session.query(sdCustomer).filter(sdCustomer.id == cust_id, sdCustomer.cust_id.is_(None)).all()
        return customer

    @staticmethod
    def get_vendors(cust_id):
        vendors = db.session.query(sdCustomer).filter(sdCustomer.cust_id == cust_id).all()
        return vendors

    @staticmethod
    def search_cust_obj(cust_id):
        customer = db.session.query(sdCustomer).filter(sdCustomer.id == cust_id).first()
        return customer
