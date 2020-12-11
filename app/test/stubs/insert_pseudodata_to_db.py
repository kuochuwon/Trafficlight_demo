import random
import time
from manage import app
from app.main import db
from app.main.model.user import sdUser
from app.main.model.device import sdDevice
from app.main.model.device_group import sdDeviceGroup
from app.main.model.issue import sdIssue
from app.main.model.issue_log import sdIssueLog
from app.main.model.code import sdCode

"""

cust_issue = db.relationship("sdIssue",
                                 primaryjoin="sdCustomer.id==sdIssue.cust_id", backref="cust1", lazy="dynamic")
vendor_issue = db.relationship("sdIssue",
                                primaryjoin="sdCustomer.id==sdIssue.vendor_id", backref="cust2", lazy="dynamic")
issues = db.relationship("sdIssue", backref="cust", lazy="dynamic")
"""


def insert_code():
    for num in range(4):
        issue_dict_log = sdCode(cust_id=5,
                                code_type=0,
                                code_no=num,
                                name="a")
        db.session.add(issue_dict_log)
    db.session.commit()


def insert_issue_log():
    issue_dict_log = sdIssueLog(issue_id=4,
                                user_id=11,
                                subject=f"民眾報修_設備號碼2",
                                description="a",
                                status_from=0,
                                status_to=0)
    db.session.add(issue_dict_log)
    for num in range(6):
        issue_dict_log = sdIssueLog(issue_id=4,
                                    user_id=11,
                                    subject=f"民眾報修_設備號碼2",
                                    description="a",
                                    status_from=num,
                                    status_to=num+1)
        db.session.add(issue_dict_log)
    db.session.commit()


def insert_issue():
    for num in range(3):
        issue_dict = sdIssue(issue_no=f"20000{num+1}",
                             category_id=num+1,
                             subject=f"民眾報修_設備號碼{num+1}",
                             description="快來修 這裡好暗",
                             cust_id=1,
                             device_id=num+2,
                             status_id=0,
                             vendor_id=6,
                             report_from="3",
                             reporter=f"王曉{num+1}",
                             reporter_email="kuochabc@gmail.com",
                             reporter_mobile="0912345678",
                             reporter_phone="02-12345678",
                             reporter_line_id=f"kkbox123{num+1}")
        db.session.add(issue_dict)
    db.session.commit()


def update_device_status():
    obj = db.session.query(sdDevice).filter(sdDevice.cust_id == 2).all()
    cunt = 0
    total = 0
    threshold = 10000
    for device in obj:
        if cunt % 4 == 0:
            status = 0
        elif cunt % 4 == 1:
            status = 4
        elif cunt % 4 == 2:
            status = 8
        elif cunt % 4 == 3:
            status = 12
        device.status = status
        cunt += 1
        if cunt == threshold:
            db.session.commit()
            cunt = 0
            total += threshold
            print(f"commit about {total}th times!")
    db.session.commit()


def insert_device():
    for num in range(100000):
        obj = sdDevice()
        obj.name = f"Newdevice_{num}"
        db.session.add(obj)
    db.session.commit()




if __name__ == "__main__":
    app.config.from_object("app.main.config.DevelopmentConfig")
    insert_code()
