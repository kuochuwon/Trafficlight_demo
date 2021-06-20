from sqlalchemy.sql import func, or_

from app.main import db
from app.main.model.issue import sdIssue
from app.main.model.user import sdUser
from app.main.constant import Constant


class sdIssueLog(db.Model):
    __tablename__ = "sd51_issue_logs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, nullable=False, comment="Sequence number of issue log")
    issue_id = db.Column(db.Integer, db.ForeignKey(sdIssue.id), nullable=False, comment="Issue id")
    user_id = db.Column(db.Integer, db.ForeignKey(sdUser.id), nullable=False,
                        comment="User id, who creates the issue log")
    subject = db.Column(db.String(50), nullable=False, comment="Issue subject")
    description = db.Column(db.Text, comment="Issue description")
    create_time = db.Column(db.DateTime, server_default=func.now(), comment="Create time")
    update_time = db.Column(db.DateTime, server_default=func.now(), comment="Update time")
    status_from = db.Column(db.Integer, nullable=False, comment="Current state")
    status_to = db.Column(db.Integer, comment="Next state")

    @staticmethod
    def add(cust_id, issue_log):
        issue = db.session.query(sdIssue).filter(sdIssue.cust_id == cust_id,
                                                 sdIssue.id == issue_log.get("issue_id")).first()

        max_sequence = issue.issue_logs.all()
        sequence = 1
        # find the max sequence of log
        if max_sequence:
            sequence = max(issue.issue_logs.all(), key=lambda log: log.sequence).sequence + 1

        status = issue_log.get("status_to")
        obj = sdIssueLog()
        obj.sequence = sequence
        obj.issue = issue
        obj.user_id = issue_log.get("user_id")
        obj.subject = issue_log.get("subject")
        obj.description = issue_log.get("description")
        obj.status_from = issue_log.get("status_from")

        # if status to is None, save status_to None and no change status in issue.
        obj.status_to = status
        if status:
            issue.set_status(status)
        return issue, obj

    @staticmethod
    def add_issue_log(cust_id, data, user_id):
        issue = db.session.query(sdIssue).filter(or_(sdIssue.cust_id == cust_id, sdIssue.vendor_id == cust_id),
                                                 sdIssue.id == data.get("id")).first()

        status = issue.status_id
        max_sequence = issue.issue_logs.all()
        sequence = 1
        # find the max sequence of log
        if max_sequence:
            sequence = max(issue.issue_logs.all(), key=lambda log: log.sequence).sequence + 1

        log = sdIssueLog()
        log.sequence = sequence
        log.issue = issue
        log.user_id = user_id
        log.subject = data.get("subject")
        log.description = data.get("description")
        log.status_from = status
        log.status_to = status
        return issue, log

    @staticmethod
    def add_dispatch_change_status(status_from, status_to, cust_id, user_id, data):
        issue = db.session.query(sdIssue).filter(or_(sdIssue.cust_id == cust_id, sdIssue.vendor_id == cust_id),
                                                 sdIssue.id == data.get("id")).first()

        max_sequence = issue.issue_logs.all()
        sequence = 1
        # find the max sequence of log
        if max_sequence:
            sequence = max(issue.issue_logs.all(), key=lambda log: log.sequence).sequence + 1

        log = sdIssueLog()
        log.sequence = sequence
        log.issue = issue
        log.user_id = user_id
        log.subject = Constant.ISSUE_CHANGE_DESC
        log.description = data.get("description")
        log.status_from = status_from
        log.status_to = status_to
        return log
