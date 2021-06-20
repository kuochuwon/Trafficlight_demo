import os
from app.main import db, create_app
from sqlalchemy.sql import text
from random import random
get_device_template = """
    SELECT * FROM sd21_devices WHERE dev_type = 1
"""

insert_device = """
    INSERT INTO sd21_devices ("name", display_name, "comment", dev_type, cust_id,  wgs_x, wgs_y)
    VALUES (:name, :display_name, :comment, :dev_type, :cust_id, :wgs_x, :wgs_y)
"""


def insert_device_by_template():
    app = create_app(os.getenv("FLASK_CONFIG") or "development")

    # Use with app.app_context() to push an application context when creating the tables.
    app.app_context().push()
    with app.app_context():
        template_device = db.session.execute(get_device_template).fetchall()
        for device_obj in template_device:
            for i in range(10):
                num = int(random()*10000)
                name = f"DEV_{num}"
                wgs_x = device_obj[-3]
                wgs_y = device_obj[-2]
                address = device_obj[-1]
                area = address[:6]
                display_name = f"{area}_{num}"
                comment = "Demy devices"
                dev_type = 2
                cust_id = 2
                db.session.execute(insert_device, {"name": name,
                                                   "display_name": display_name,
                                                   "comment": comment,
                                                   "dev_type": dev_type,
                                                   "cust_id": cust_id,
                                                   "wgs_x": wgs_x,
                                                   "wgs_y": wgs_y})
        db.session.commit()


if __name__ == "__main__":
    insert_device_by_template()
