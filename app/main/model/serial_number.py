import re
import datetime

from app.main import db
from app.main.model.customer import sdCustomer


class sdSerialNumber(db.Model):
    __tablename__ = "sd52_serial_number"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_id = db.Column(db.Integer, db.ForeignKey(sdCustomer.id), nullable=False, comment="Customer id")
    prefix = db.Column(db.String(20), nullable=False, comment="Prefix words")
    serial_no = db.Column(db.Integer, nullable=False, comment="Serial number")

    __table_args__ = (db.UniqueConstraint("cust_id", "prefix", "serial_no"),)

    def __repr__(self):
        return f"<sdSerialNumber id={self.id}/cust_id={self.cust_id}/prefix={self.prefix}/serial_no={self.serial_no}>"

    @staticmethod
    def get_serial_no(cust_id, prefix):
        obj = db.session.query(sdSerialNumber).filter(sdSerialNumber.cust_id == cust_id,
                                                      sdSerialNumber.prefix == prefix).first()
        if not obj:
            obj = sdSerialNumber()
            obj.cust_id = cust_id
            obj.prefix = prefix
            obj.serial_no = 1

        else:
            obj.serial_no = obj.serial_no + 1

        db.session.add(obj)

        return obj.serial_no

    @staticmethod
    def conv_serial_no(cust_id):
        """
        :param cust_id: cust_id
        :var namespace: CUSTOM-{datetime:%Y%m%d}-{serial_no:05d}
        :var prefix: CUSTOM-{datetime:%Y%m%d}-
        :var serial_no example: 1
        :return example: CUSTOM-20200130-00001
        """
        cust = sdCustomer.query.filter(sdCustomer.id == cust_id).first()
        # regex to get words
        words = re.split(r"[{](.*?)[}]", cust.issue_namespace)

        # find specific in rule
        date_time = next(s for s in words if "datetime" in s)
        sn = next(s for s in words if "serial_no" in s)

        # compose prefix: cust naming + datetime
        date = datetime.datetime.now()
        conv_time = date.strftime(date_time.split(":")[1])
        prefix = "".join([word for word in words if "serial_no" not in word])
        prefix = prefix.replace(date_time, conv_time)
        serial_no = sdSerialNumber.get_serial_no(cust_id, prefix)

        # format to :d digits
        sq_rule, digits = sn.split(":")
        digits = "{:" + digits + "}"
        sequence = digits.format(serial_no)

        serial_number = prefix + sequence
        return serial_number
