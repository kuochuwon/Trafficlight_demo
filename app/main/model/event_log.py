from sqlalchemy.sql import func, or_

from app.main import db
from app.main.constant import map_status
from app.main.model.device import sdDevice


class sdEventLog(db.Model):
    __tablename__ = "sd53_event_logs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, db.ForeignKey("sd21_devices.id"), nullable=False, comment="Device_id")
    status_id = db.Column(db.Integer,
                          nullable=False, comment="info, normal, warning or error")
    component_id = db.Column(db.Integer,
                             nullable=False, comment="component of device in the event")
    category_id = db.Column(db.Integer, nullable=False, comment="Event type")
    description = db.Column(db.Text, comment="event description")
    cust_id = db.Column(db.Integer, db.ForeignKey("sd10_customers.id"), nullable=False, comment="Customer id")
    create_time = db.Column(db.DateTime, server_default=func.now(), comment="Create time")
    update_time = db.Column(db.DateTime, server_default=func.now(), comment="Update time")
    data_time = db.Column(db.DateTime, server_default=func.now(), comment="device data time")
    replace_id = db.Column(db.Integer, db.ForeignKey("sd53_event_logs.id"), comment="Event id that become normal")
    ack = db.Column(db.Integer, nullable=False, comment="0 = unread, 1 = read")

    # TODO should connect with issue model later
    # issues = db.relationship("sdIssue", backref="eventlog", lazy="dynamic")

    def __repr__(self):
        return f"<sdEventLog id={self.id}/cust_id={self.cust_id}/device_id = {self.device_id}>"

    @staticmethod
    def get_id_by_name(keyword_list):
        devices = []
        for keyword in keyword_list:
            keyword = "%{}%".format(keyword)
            # ilike: case insensitive
            devices.extend(db.session.query(sdDevice).filter(sdDevice.name.ilike(keyword)).all())

        id_list = [device.id for device in devices]
        return id_list

    @staticmethod
    def get_basequery(sort_by, order_by):
        if sort_by == "device_name":
            stmt = db.session.query(sdEventLog)\
                .join(sdEventLog, sdDevice.event_logs)\
                .order_by(getattr(sdDevice.name, order_by)())

        else:
            if order_by == "asc":
                stmt = db.session.query(sdEventLog)\
                    .order_by(getattr(sdEventLog, sort_by).asc())
            elif order_by == "desc":
                stmt = db.session.query(sdEventLog)\
                    .order_by(getattr(sdEventLog, sort_by).desc())
        return stmt

    @staticmethod
    def get(cust_id, event_condtion):
        """about variable pagination:
            1. sdEventLog.device.has(vendor_id=cust_id):
                To find obj match the vendor_id through relationship: sdEventLog.device
            2. (*filter_conditions):
                To store many filter criterias
            3. paginate:
                Pagination module in sqlalchemy
        """

        current_pages = event_condtion.get("page")
        items_per_page = event_condtion.get("limit")
        filter_condition = event_condtion.get("filter")
        sort_by = event_condtion.get("sort_by")
        order_by = event_condtion.get("order_by")
        time_interval = event_condtion.get("time_interval")
        stime, etime = time_interval[0], time_interval[1]

        # TAG generate filter conditions
        filter_conditions = []
        for key, value in filter_condition.items():
            if key == "device_name":
                value = sdEventLog.get_id_by_name(value)
                key = "device_id"
            filter_conditions.append(getattr(sdEventLog, key).in_(value))
        filter_conditions.append((sdEventLog.create_time >= stime) & (sdEventLog.create_time < etime))

        filter_conditions = tuple(filter_conditions)

        stmt = sdEventLog.get_basequery(sort_by, order_by)

        pagination = stmt.filter(or_(sdEventLog.device.has(vendor_id=cust_id),
                                     sdEventLog.cust_id == cust_id),
                                 (*filter_conditions))\
            .paginate(current_pages, items_per_page, False)

        # total pages
        pages = pagination.pages

        # total items
        total_found = pagination.total

        # result of current condition
        query = pagination.items

        item_number_cust = db.session.query(func.count(sdEventLog.id)).filter(sdEventLog.cust_id == cust_id).scalar()

        return query, pages, total_found, item_number_cust

    @staticmethod
    def getdetail(cust_id, event_list):
        query = db.session.query(sdEventLog).filter(or_(sdEventLog.cust_id == cust_id,
                                                        sdEventLog.device.has(vendor_id=cust_id)),
                                                    sdEventLog.id.in_(event_list)).all()
        return query

    @staticmethod
    def acknowledge(cust_id, event_list):
        query = db.session.query(sdEventLog).filter(sdEventLog.cust_id == cust_id,
                                                    sdEventLog.id.in_(event_list)).all()
        for event in query:
            event.ack = 1
        return query

    @staticmethod
    def getnotice(cust_id):
        warning = map_status("WARNING")
        error = map_status("ERROR")
        eventlogs = db.session.query(sdEventLog)\
            .order_by(sdEventLog.create_time.desc())\
            .filter(or_(sdEventLog.cust_id == cust_id,
                        sdEventLog.device.has(vendor_id=cust_id)),
                    sdEventLog.replace_id.is_(None),
                    sdEventLog.ack == 0,
                    sdEventLog.status_id.in_([warning, error])).limit(50).all()

        # TAG scalar means it will just catch value, not object
        error_count = db.session.query(func.count(sdEventLog.id)).filter(or_(sdEventLog.cust_id == cust_id,
                                                                             sdEventLog.device.has(vendor_id=cust_id)),
                                                                         sdEventLog.replace_id.is_(None),
                                                                         sdEventLog.status_id == error).scalar()
        warning_count = db.session.query(func.count(sdEventLog.id)).filter(or_(sdEventLog.cust_id == cust_id,
                                                                               sdEventLog.device.has(vendor_id=cust_id)),
                                                                           sdEventLog.replace_id.is_(None),
                                                                           sdEventLog.status_id == warning).scalar()
        return eventlogs, error_count, warning_count
