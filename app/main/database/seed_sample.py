import os
import csv
import twd97
import uuid
from app.main import db, logger
from app.main.model.device import sdDevice
from app.main.model.device_model import sdDeviceModel
from app.main.model.device_group import sdDeviceGroup
from app.main.model.controller import sdController
from app.main.model.led import sdLed
from app.main.model.customer import sdCustomer
from app.main.model.user import sdUser

__cust_name = "ntpc"
__cust_display = "New Taipei City"
__cust_comment = "新北市政府"
__model_led = ["LM1109-I1FGT", "9KLM LED LAMP NW LUMILEDS REBEL ES CNS W/PSU"]
__model_ctrl = ["GPD002-000GT", "LED DRIVER 100W 100-277 V CE"]


def clean_data():
    # truncate sdDevice, sdController, sdLed
    cust = db.session.query(sdCustomer).filter(sdCustomer.name == __cust_name).first()
    if cust:
        db.session.execute(f"delete from {sdDevice.__tablename__} where cust_id={cust.id}")
        db.session.execute(f"delete from {sdController.__tablename__} where cust_id={cust.id}")
        db.session.execute(f"delete from {sdLed.__tablename__} where cust_id={cust.id}")
        db.session.execute(f"delete from {sdDeviceGroup.__tablename__} where cust_id={cust.id}")
        db.session.execute(
            f"delete from {sdDeviceModel.__tablename__} where name in ('{__model_led[0]}', '{__model_ctrl[0]}')")
        db.session.execute(f"delete from {sdUser.__tablename__} where cust_id={cust.id}")
        db.session.execute(f"delete from {sdCustomer.__tablename__} where id={cust.id}")
        db.session.commit()
    return


def seed_ntpc():
    logger.debug("Seed NTPC sample data")
    data_file = os.path.join(os.getcwd(), "seed", "NTCLighting.csv")
    if not os.path.isfile(data_file):
        logger.debug(f"CSV file not existed: {data_file}")
        return

    clean_data()

    # add basic data
    cust = sdCustomer(name=__cust_name, display_name=__cust_display, comment=__cust_comment)
    user = sdUser(cust=cust, name="admin", display_name="Admin (NTPC)", comment="NTPC Administrator",
                  password="AcBel.Lighting,168")
    model_led = sdDeviceModel(name=__model_led[0], display_name=__model_led[1])
    model_ctrl = sdDeviceModel(name=__model_ctrl[0], display_name=__model_ctrl[1])
    db.session.add(cust)
    db.session.add(user)
    db.session.add(model_led)
    db.session.add(model_ctrl)
    db.session.commit()

    # add devices
    device_groups = {}
    with open(data_file, encoding='utf-8', newline='') as csv_file:
        rows = csv.reader(csv_file)
        index = 0
        row_count = 0
        for row in rows:
            index += 1
            if index == 1:
                # ignore header
                continue
            # convert twd97 to wgs84
            try:
                twd_x, twd_y = float(row[4]), float(row[5])
                (wgs_y, wgs_x) = twd97.towgs84(twd_x, twd_y)
            except Exception:
                logger.debug(f"twd or wgs error: {row}")
                continue
            # check if coordination out of range
            if wgs_x < 120 or wgs_x > 122 or wgs_y < 24 or wgs_y > 26:
                logger.debug(f"wgs_x or wgs_y out of range: 120 <= x < 122 or 24 <= x < 26")
                continue
            # add device
            row_count = row_count + 1
            # get or new device group
            group_name = row[0]
            device_group = device_groups.get(group_name)
            if not device_group:
                device_group = sdDeviceGroup(cust=cust, name=group_name, display_name=f"新北市{group_name}")
                device_groups[group_name] = device_group
            # new device
            device = sdDevice(cust=cust,
                              name=f"{row_count}",
                              display_name=f"{row[0]}_{row_count}",
                              comment=f"New no is {row[1]}, Old no is {row[2]}",
                              address=f"新北市{row[3]}",
                              device_group=device_group,
                              wgs_x=wgs_x, wgs_y=wgs_y)
            # assign controller and led
            device.controller = sdController(model=model_ctrl, cust=cust, serial_no=str(uuid.uuid4()))
            device.led = sdLed(model=model_led, cust=cust, serial_no=str(uuid.uuid4()))
            # add objects
            db.session.add(device)
            if (row_count % 10000) == 0:
                db.session.commit()
                logger.debug(f"Commit {row_count}")
        db.session.commit()
        logger.debug(f"Total device committed {row_count}")
