from app.main.log import logger
from app.main.util.common import convert_null_emptystr


def dimming_convert(dimming_raw):
    if dimming_raw is None:
        return None
    level = dimming_raw // 20 + 1
    if dimming_raw == 100:
        level = 5
    return level


def get_geojson_from_sql_results(results):  # the contents here should be same with "add_device_geojson_to_db (test)"
    first_type = "FeatureCollection"
    second_type = "Feature"
    third_type = "Point"
    user_devices_json = dict(type=first_type, features=[])

    user_devices_json['features'] = [{
        "type": second_type,
        "geometry": {"type": third_type,
                     "coordinates": [wgs_x, wgs_y]},
        "properties": {"id": str(device_id),
                       "name": name,
                       "display_name": display_name,
                       "comment": comment,
                       "status": status,
                       "power_status": power_status,
                       "address": address,
                       "group_name": group_name,
                       "group_display_name": group_display_name
                       }}
        for device_id, name, display_name, comment, status, power_status, wgs_x, wgs_y, address,
        group_name, group_display_name in results]

    logger.debug("success for generate GeoJSON data.")
    convert_null_emptystr(user_devices_json)
    combined_json = {"geojson": user_devices_json}

    return combined_json
