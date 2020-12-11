from datetime import timedelta
from sqlalchemy.sql import func, or_

from app.main import db
from app.main.model.customer import sdCustomer
from app.main.model.serial_number import sdSerialNumber
from app.main.model.device import sdDevice
from app.main.model.code import sdCode
from app.main.model.event_log import sdEventLog
from app.main.model.user import sdUser
from app.main.constant import Constant


class sdIssue(db.Model):
    __tablename__ = "sd50_issues"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issue_no = db.Column(db.String(30), nullable=False, comment="Issue number")
    error_code = db.Column(db.Integer, db.ForeignKey(sdCode.id), comment="Error code id")
    priority_id = db.Column(db.Integer, db.ForeignKey(sdCode.id), comment="Priority id")
    subject = db.Column(db.String(50), nullable=False, comment="Issue subject")
    description = db.Column(db.Text, comment="Issue description")
    create_time = db.Column(db.DateTime, server_default=func.now(), comment="Create time")
    update_time = db.Column(db.DateTime, server_default=func.now(), comment="Update time")
    due_day = db.Column(db.Date, comment="Expected time for dispatching")
    cust_id = db.Column(db.Integer, db.ForeignKey(sdCustomer.id), nullable=False, comment="Customer id")
    device_id = db.Column(db.Integer, db.ForeignKey(sdDevice.id), nullable=False, comment="Device id")
    status_id = db.Column(db.Integer, db.ForeignKey(sdCode.id), nullable=False, comment="Status id")
    vendor_id = db.Column(db.Integer, db.ForeignKey(sdCustomer.id), comment="Vendor id")
    event_id = db.Column(db.Integer, comment="Event log id")
    assignee_id = db.Column(db.Integer, db.ForeignKey(sdUser.id),
                            comment="Assignee id, who is responsible for the dispatching")
    report_from = db.Column(db.Integer, db.ForeignKey(sdCode.id), nullable=False, comment="Report source")
    reporter = db.Column(db.String(20), comment="Reporter name")
    reporter_email = db.Column(db.String(100), comment="Reporter email")
    reporter_mobile = db.Column(db.String(15), comment="Reporter mobile phone")
    reporter_phone = db.Column(db.String(15), comment="Telephone telephone")
    reporter_line_id = db.Column(db.String(64), comment="LINE id")

    issue_logs = db.relationship("sdIssueLog", backref="issue", lazy="dynamic")

    __table_args__ = (db.UniqueConstraint("cust_id", "issue_no"),)

    def __repr__(self):
        return f"<sdIssue id={self.id}/issue_no={self.issue_no}>"

    def set_status(self, status):
        # If change status, there would be some action here.
        self.status_id = status

    @staticmethod
    def get_due_days(priority_name):
        day = Constant.PRIORITY_DUE_DAY.get(priority_name)
        working_days = timedelta(days=day)
        return working_days

    @staticmethod
    def getdetail(cust_id, issue_list, role_set):
        detail_issues = []
        for role in role_set:
            if role == Constant.SYSTEM_ADMIN:
                detail_issues = db.session.query(sdIssue).filter(sdIssue.id.in_(issue_list)).all()
            else:
                statuses = Constant.ACCESS_PRIVILEGES.get(role)
                query = db.session.query(sdIssue).filter(
                    or_(sdIssue.cust_id == cust_id, sdIssue.vendor_id == cust_id),
                    sdIssue.id.in_(issue_list)
                ).all()
                detail_issues.extend([obj for obj in query if obj.status.name in statuses])
        return list(set(detail_issues))

    @staticmethod
    def add(cust_id, issue):
        obj = sdIssue()

        priority_info_list = sdCode.get_code_bytype(cust_id, Constant.CODE_TYPE_ISSUE_PRIORITY)
        reference = {priority.name: priority.id for priority in priority_info_list}
        device = db.session.query(sdDevice).filter(sdDevice.id == issue.get("device_id")).first()

        obj.issue_no = sdSerialNumber.conv_serial_no(cust_id)
        obj.error_code = issue.get("error_code")
        obj.subject = issue.get("subject")
        obj.description = issue.get("description")
        obj.cust_id = cust_id
        obj.device_id = device.id

        obj.status_id = issue.get("issue_status_id")
        obj.vendor_id = device.vendor_id
        obj.priority_id = reference.get("normal")
        obj.report_from = issue.get("report_from")
        obj.reporter = issue.get("reporter")
        obj.reporter_email = issue.get("reporter_email")
        obj.reporter_mobile = issue.get("reporter_mobile")
        obj.reporter_phone = issue.get("reporter_phone")

        # for getting the priority name
        db.session.add(obj)
        db.session.flush()
        obj.due_day = obj.create_time + sdIssue.get_due_days(obj.priority.name)
        return obj

    @staticmethod
    def getall(cust_id, role_set):

        all_issues = []
        for role in role_set:
            if role == Constant.SYSTEM_ADMIN:
                all_issues = db.session.query(sdIssue).all()
            else:
                statuses = Constant.ACCESS_PRIVILEGES.get(role)
                query = db.session.query(sdIssue).filter(
                    or_(sdIssue.cust_id == cust_id, sdIssue.vendor_id == cust_id)).all()
                all_issues.extend([obj for obj in query if obj.status.name in statuses])
        # remove duplicate items
        return list(set(all_issues))

    @staticmethod
    def update(cust_id, id, assignee_id, priority_id, new_status):
        obj = db.session.query(sdIssue).filter(or_(sdIssue.cust_id == cust_id, sdIssue.vendor_id == cust_id),
                                               sdIssue.id == id).first()
        old_status = obj.status_id

        obj.status_id = new_status
        obj.assignee_id = assignee_id
        obj.priority_id = priority_id
        obj.due_day = obj.create_time + sdIssue.get_due_days(obj.priority.name)
        return old_status, new_status
