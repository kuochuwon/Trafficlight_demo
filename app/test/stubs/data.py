from app.main import db
from app.main.service import ret
from app.main.model.led import sdLed
from app.main.model.user import sdUser
from app.main.model.issue import sdIssue
from app.main.model.controller import sdController
from app.main.model.customer import sdCustomer
from app.main.model.device_model import sdDeviceModel
from app.main.model.schedule_group import sdScheduleGroup
from app.main.model.schedule_item import sdScheduleItem
from app.main.model.user_group import sdUserGroup
from app.main.model.issue_log import sdIssueLog
from app.main.model.event_log import sdEventLog
from app.main.model.roles import sdRole
from app.main.model.code import sdCode

# Insert fake data to test db


class FakeDataCreation(object):
    group_count = None
    schedule_group = None
    issues = None

    def __init__(self):
        # In the base test, there are cust_id = 1 and user_id = 1 test customer
        self.cust = 1
        self.user = 1

    def insert_device(self, number):
        from app.main.model.device import sdDevice
        import datetime

        # insert device model
        self.insert_device_model(number)
        # insert led
        self.insert_led(number)
        # insert controller
        self.insert_controller(number)

        # insert device
        divisor = number // self.group_count
        for device in range(number):
            obj = sdDevice(name=f"testname_{device+1}",
                           display_name="奇岩的路燈",
                           comment="測試留言武功蓋世，世界大亂鬥。(){}@#$&*^",
                           create_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           update_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           status=0,
                           power_status=1,
                           dimming=50,
                           cust_id=self.cust,
                           wgs_x=121.8,
                           wgs_y=21.5,
                           controller_id=device+1,
                           led_id=device+1,
                           device_group_id=device // divisor + 1)
            db.session.add(obj)
        db.session.commit()
        db.session.close()
        return self

    def insert_device_group(self, dg_no, ug_no):
        from app.main.model.device_group import sdDeviceGroup
        if not isinstance(dg_no, int):
            raise Exception("number should be integer!")

        # set device.device_group_id by yourself
        self.group_count = dg_no

        # prevent other test broken. others didn't insert schedule
        groups = [None for i in range(dg_no)]
        if self.schedule_group:
            groups = [i for i in range(1, self.schedule_group)] * dg_no
        name = 1
        for each_id in range(dg_no):

            obj = sdDeviceGroup(name=f"testgroup_{each_id+1}",
                                display_name="test_streetlight",
                                create_time="2019-12-18",
                                update_time="2019-12-18",
                                schedule_id=groups[each_id],
                                cust_id=self.cust)
            if ug_no != 0:
                for i in range(1, ug_no):
                    user_group = sdUserGroup(
                        name=f"test_user_group{name}",
                        display_name=f"測試ug{name}",
                        comment="測試的使用者群組",
                        create_time="2020-02-11",
                        update_time="2020-02-11",
                        cust_id=self.cust,
                    )

                    obj.user_groups.append(user_group)
                    name += 1
            db.session.add(obj)

        db.session.commit()
        return self

    def insert_other_user(self):
        cust = sdCustomer(
            name="testcust2",
            display_name="Test Customer",
            comment="For Unit Test"
        )
        db.session.add(cust)
        db.session.commit()

    def insert_issue_cust1(self, number):
        self.issues = number
        for i in range(1, number):
            issue = sdIssue(
                issue_no=f"TX00{i}",
                error_code=9,
                subject=f"TX00{i} 報修單",
                description="抱抱抱修單",
                priority_id=12,
                create_time="2020-01-07",
                update_time="2020-01-07",
                cust_id=1,
                device_id=1,
                status_id=1,
                vendor_id=(i % 2),
                assignee_id=1,
                report_from=1,
                reporter="大名",
                reporter_email="@123",
                reporter_mobile="0931",
                reporter_phone="0988",
                reporter_line_id=""
            )

            db.session.add(issue)
        db.session.commit()
        return self

    def insert_controller(self, number):
        for controller in range(0, number):
            new_controller = sdController(
                name=f"test_controller_{controller+1}",
                display_name="奇岩的controller",
                comment="For Unit Test",
                create_time="2019-12-18",
                update_time="2019-12-18",
                cust_id=self.cust,
                serial_no="BX000{}".format(controller+1)
            )
            db.session.add(new_controller)
        db.session.commit()

    def insert_led(self, number):
        for led in range(0, number):
            new_led = sdLed(
                name=f"test_led_{led+1}",
                display_name="Test User",
                comment="For Unit Test",
                create_time="2019-12-18",
                update_time="2019-12-18",
                serial_no="BX000{}".format(led+1),
                cust_id=self.cust
            )

            db.session.add(new_led)
        db.session.commit()

    def insert_device_model(self, number):
        for i in range(number):
            device_model = sdDeviceModel(
                name="test_device_model",
                display_name="Test Device Model",
                comment="For Unit Test"
            )

            db.session.add(device_model)
            db.session.commit()

    def insert_schedule_group(self, number):
        scheme = ["24h", "srss"] * number
        self.schedule_group = number
        for i in range(number):
            schedule_group = sdScheduleGroup(
                name=f"schedule_{i}",
                display_name="test_display_name",
                comment="For Unit Test",
                scheme=scheme[i],
                incre="y",
                cust_id=self.cust
            )

            db.session.add(schedule_group)
        db.session.commit()

        return self

    def insert_schedule_item(self):
        days = ["0", "1", "2", "3", "4"]
        time_stamp = ["13:00", "15:00", "17:00", "21:00", "23:00"]
        dimming = ["10", "30", "50", "70", "90"]
        for i in range(1, self.schedule_group):
            # run 5 time insert 5 time per day
            for day in days:
                for time, dim in zip(time_stamp, dimming):
                    schedule_item = sdScheduleItem(
                        day=day,
                        time=time,
                        dimming=dim,
                        schedule_group_id=i,
                        cust_id=self.cust
                    )

                    db.session.add(schedule_item)
        db.session.commit()

        return self

    def insert_issue(self, number):
        self.issues = number
        for i in range(1, number):
            issue = sdIssue(
                issue_no=f"TX00{i}",
                error_code=9,
                subject=f"TX00{i} 報修單",
                description="抱抱抱修單",
                priority_id=13,
                due_day="2020-01-11",
                create_time="2020-01-07",
                update_time="2020-01-07",
                cust_id=self.cust,
                device_id=1,
                status_id=1,
                vendor_id=(i % 2),
                assignee_id=1,
                report_from=1,
                reporter="大名",
                reporter_email="@123",
                reporter_mobile="0931",
                reporter_phone="0988",
                reporter_line_id=""
            )

            db.session.add(issue)
        db.session.commit()

        return self

    def insert_issue_log(self):
        status = [(1, 2), (2, 3), (3, 3), (3, 4), (4, 5), (5, 6)]
        for i in range(1, self.issues):
            sequence = 1
            for s in status:
                issue_log = sdIssueLog(
                    issue_id=i,
                    sequence=sequence,
                    user_id=self.user,
                    subject=f"TX00{i} 報修單之log ({s[1]})",
                    description="issue log",
                    create_time="2020-01-10",
                    update_time="2020-01-10",
                    status_from=s[0],
                    status_to=s[1],
                )
                sequence += 1

                db.session.add(issue_log)
        db.session.commit()

        return self

    def insert_code_spec(self):
        issue_status = {0: ("new", "NEW"),
                        1: ("acknowledged", "ACKNOWLEDGED"),
                        2: ("assigned", "ASSIGNED"),
                        3: ("progress", "IN - PROGRESS"),
                        4: ("resolved", "RESOLVED"),
                        5: ("closed", "CLOSED")}
        issue_category = {0: ("not_working", "燈不亮"),
                          1: ("flashing_fault", "燈閃爍"),
                          2: ("others", "其他")}
        report_from = {0: "admin",
                       1: "anonymous",
                       2: "people"}
        priority = {
            0: ("normal", "普通"),
            1: ("high", "速件"),
            2: ("urgent", "最速件")
        }

        for key, item in issue_status.items():
            status = sdCode(
                cust_id=self.cust,
                code_type=0,
                code_no=key,
                name=item[0],
                display_name=item[1],
                create_time="2020/02/11",
                update_time="2020/02/11"
            )
            db.session.add(status)

        for key, item in issue_category.items():
            category = sdCode(
                cust_id=self.cust,
                code_type=1,
                code_no=key,
                name=item[0],
                display_name=item[1],
                create_time="2020/02/11",
                update_time="2020/02/11"
            )
            db.session.add(category)

        for key, item in report_from.items():
            report = sdCode(
                cust_id=self.cust,
                code_type=2,
                code_no=key,
                name=item,
                display_name=item,
                create_time="2020/02/11",
                update_time="2020/02/11"
            )

            db.session.add(report)
        for key, item in priority.items():
            pri = sdCode(
                cust_id=self.cust,
                code_type=6,
                code_no=key,
                name=item[0],
                display_name=item[1],
                create_time="2020/02/11",
                update_time="2020/02/11"
            )
            db.session.add(pri)
        db.session.commit()
        return self

    def user_for_issue(self):
        cust = sdCustomer(
            id=0,
            name="admin",
            display_name="Test Customer",
            comment="For Unit Test",
            issue_namespace="NTPC-{datetime:%Y%m%d}-{serial_no:05d}"
        )
        self.cust = 0
        anonymous = sdUser(
            name="anonymous",
            display_name="anonymous",
            password="Test Password",
            comment="For Test Issue"
        )
        usergroup = sdUserGroup(
            name="a group",
            display_name="Test User"
        )

        role = db.session.query(sdRole).filter(sdRole.id == "1").first()

        self.user = 2

        cust.users.append(anonymous)
        anonymous.user_groups.append(usergroup)
        usergroup.rel_role_ug.append(role)
        db.session.add(cust)
        db.session.commit()
        return self

    def insert_event_log(self):
        status = [12, 13, 14, 13, 14]
        for e in range(1, 3):
            for s in status:
                even_log = sdEventLog(
                    device_id=e,
                    status_id=s,
                    component_id=1,
                    category_id=0,
                    description="測試用描述",
                    cust_id=self.cust,
                    create_time="2020-02-06",
                    update_time="2020-02-06",
                    ack=0
                )

                db.session.add(even_log)
        db.session.commit()

        return self

    def insert_event_log_roy(self):
        status = [0, 4, 8, 4, 8]
        id_list = [5, 10]
        for e in range(1, 3):
            for s in status:
                even_log = sdEventLog(
                    device_id=e,
                    status_id=s,
                    component_id=0,
                    category_id=0,
                    description="測試用描述",
                    cust_id=self.cust,
                    create_time="2020-02-06",
                    update_time="2020-02-06",
                    replace_id="1",
                    ack=0
                )
                db.session.add(even_log)
        for i in id_list:
            obj = db.session.query(sdEventLog).filter(sdEventLog.id == i).first()
            obj.replace_id = None
            db.session.add(even_log)
        db.session.commit()

        return self


class ExpectResponse(object):

    def __init__(self):
        self.response_body = None
        self.number = None
        self.device_groups = []
        self.device = None

    def compose_response_body(self):
        self.response_body = ret.http_resp(ret.RET_OK)
        return self

    # designate group nad device quantity
    def count(self, number, device):
        self.number = number
        self.device = device
        return self

    def group_id(self):
        if not self.device_groups:
            for group_id in range(self.number):
                group_id = group_id + 1
                self.device_groups.append({"id": str(group_id)})
            return self

        if self.device_groups:
            for count, group_id in zip(range(self.number), self.device_groups):
                group_id = group_id + 1
                self.device_groups[count]["id"] = str(group_id)

        return self

    def name(self):
        if not self.device_groups:
            for name in range(self.number):
                self.device_groups.append({"name": f"testgroup_{name+1}"})
            return self

        if self.device_groups:
            for count, name in zip(range(self.number), self.device_groups):
                self.device_groups[count]["name"] = f"testgroup_{count+1}"

        return self

    def display_name(self):
        for count in range(self.number):
            self.device_groups[count]["display_name"] = "test_streetlight"

        return self

    def user_groups(self):
        # This part of API is not Implement
        for count in range(self.number):
            self.device_groups[count]["user_groups"] = []
        return self

    def schedule_groups(self):
        # This part of API is not Implement
        for count in range(self.number):
            self.device_groups[count]["schedule_groups"] = []
        return self

    def devices(self):
        divisor = self.device // self.number
        # compose expect to [{1:[1, 2, 3, ..]}, ...]
        devices = {}
        for x, y in [[device // divisor + 1, device + 1] for device in range(0, self.device)]:
            if x in devices:
                # TAG change str here
                devices[x].append(str(y))
            else:
                # TAG change str here
                devices[x] = [str(y)]

        for group_id, devices in devices.items():
            self.device_groups[group_id-1]["devices"] = devices
        return self

    def response(self):
        # compose response
        response = self.response_body
        response["device_groups"] = self.device_groups
        return response

    def many_counts(self):
        for count in range(self.number):
            self.device_groups[count]["device_count"] = 4
            self.device_groups[count]["warning_count"] = 0
            self.device_groups[count]["error_count"] = 0
            self.device_groups[count]["poweroff_count"] = 0
        return self


def compose_input_for_device(number):
    devices = []
    for device in range(number):
        devices.append(dict(id=f"{device+1}",
                            name=f"testname_{device+1}",
                            display_name="淡水廠的路燈",
                            comment="這是測試device的小天地，@#$%^&*[]_=+-*",
                            wgs_x=27.0,
                            wgs_y=29.0,
                            address="write something",
                            controller={"model_name": "GPD002-000GT",
                                        "name": "A{}".format(100 + device),
                                        "display_name": "2019/12/4",
                                        "comment": "controller good",
                                        "serial_no": "BX000{}".format(device+1)},
                            led={"model_name": "LM1109-I1FGT",
                                 "name": "A{}".format(100 + device),
                                 "display_name": "2019/12/4",
                                 "comment": "led good",
                                 "serial_no": "BX000{}".format(device+1)}
                            ))
    data = dict(devices=devices)
    return data


def compose_input_for_schedule(number):
    schedules = []
    for schedule in range(number):
        schedules.append(dict(name=f"SG_{schedule}",
                              display_name=f"My_SG_{schedule}",
                              comment="leave message",
                              scheme="24h",
                              incre="n",
                              schedule_days={"0": {"00:00": 60,
                                                   "06:00": 0,
                                                   "17:00": 40,
                                                   "19:00": 100},
                                             "1": {"00:00": 60,
                                                   "06:00": 0,
                                                   "17:00": 40,
                                                   "19:00": 100}}
                              ))
    data = dict(schedule_groups=schedules)
    return data
