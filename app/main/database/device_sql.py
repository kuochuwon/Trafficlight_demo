from app.main import db
from app.main.log import logger
from sqlalchemy.sql import text

sql_get_all_device = """
    SELECT
        sd21.id, sd21.name, sd21.display_name, sd21.comment,
        sd21.status, sd21.power_status, sd21.wgs_x, sd21.wgs_y, sd21.address, sd22_device_groups.name,
        sd22_device_groups.display_name
    FROM
        sd21_devices AS sd21
    LEFT JOIN sd22_device_groups
        ON sd21.device_group_id=sd22_device_groups.id
    WHERE sd21.cust_id = :cust_id OR sd21.vendor_id = :vendor_id
    """


sql_get_limit_device = f"{sql_get_all_device} LIMIT :remaining"

sql_get_all_summary = """
    SELECT
        b.id, b.name AS device_group_name, b.display_name AS device_group_display_name,
        coalesce(a.device_count, 0) device_count,
        coalesce(a.poweroff_count, 0) poweroff_count,
        coalesce(a.warning_count, 0) warning_count,
        coalesce(a.error_count, 0) error_count
    FROM
        sd22_device_groups AS b LEFT JOIN
        (
            SELECT
                device_group_id,
                count(*) device_count,
                count(*) FILTER (WHERE (power_status = 0)) poweroff_count,
                count(*) FILTER (WHERE (status & 4)>0) warning_count,
                count(*) FILTER (WHERE (status & 8)>0) error_count
            FROM sd21_devices GROUP BY device_group_id
        )
        AS a ON b.id = a.device_group_id
    WHERE cust_id = :cust_id
"""


def getall_devicelist_for_geojson(cust, user, number):
    if (cust and user) and (number == 0):
        try:
            results = db.session.execute(sql_get_all_device, {"cust_id": cust, "vendor_id": cust}).fetchall()

            logger.debug("success for get data from SQL")
            return results
        except Exception as e:
            logger.error(f"failed for get data from SQL: {str(e)}")
            db.session.rollback()
            raise
        finally:
            db.session.close()
    elif cust and user:
        try:
            results = db.session.execute(text(sql_get_limit_device), {
                                         "cust_id": cust, "vendor_id": cust, "remaining": number}).fetchall()
            logger.debug("success for get data from SQL")
            return results
        except Exception as e:
            logger.error(f"failed for get data from SQL: {str(e)}")
            db.session.rollback()
            raise
        finally:
            db.session.close()


def get_all_summary_table(cust):
    try:
        results = db.session.execute(sql_get_all_summary, {"cust_id": cust}).fetchall()
        logger.debug("success for get data from SQL")
        return results
    except Exception as e:
        logger.error(f"failed for get data from SQL: {str(e)}")
    finally:
        db.session.close()
