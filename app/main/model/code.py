from sqlalchemy.sql import func

from app.main import db
from app.main.model.customer import sdCustomer


class sdCode(db.Model):
    __tablename__ = "sd12_codes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_id = db.Column(db.Integer, db.ForeignKey(sdCustomer.id), nullable=False, comment="Customer id")
    code_type = db.Column(db.Integer, comment="Code type, specification write in constant")
    code_no = db.Column(db.Integer, nullable=False, comment="Code number")
    name = db.Column(db.String(20), nullable=False, comment="Code name")
    display_name = db.Column(db.String(50), comment="Code display name")
    create_time = db.Column(db.DateTime, server_default=func.now(), comment="Create time")
    update_time = db.Column(db.DateTime, server_default=func.now(), comment="Update time")

    # priority_issues = db.relationship(
    #     "sdIssue", foreign_keys="sdIssue.priority_id", backref="priority", lazy="dynamic")
    # error_issues = db.relationship(
    #     "sdIssue", foreign_keys="sdIssue.error_code", backref="error", lazy="dynamic")
    # status_issues = db.relationship(
    #     "sdIssue", foreign_keys="sdIssue.status_id", backref="status", lazy="dynamic")
    # report_source_issues = db.relationship(
    #     "sdIssue", foreign_keys="sdIssue.report_from", backref="report_source", lazy="dynamic")

    @staticmethod
    def get_codes(cust_id):
        codes = db.session.query(sdCode).filter(sdCode.cust_id == cust_id).all()
        return codes

    @staticmethod
    def get_code_bytype(cust_id, code_type):
        codes = db.session.query(sdCode).filter(sdCode.cust_id == cust_id,
                                                sdCode.code_type == code_type).all()
        return codes
