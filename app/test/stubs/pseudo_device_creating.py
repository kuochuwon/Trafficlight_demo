from app.main import db
from app.main.model.device import sdDevice
from app.main.model.roles import sdRole
from app.main.model.user_group import sdUserGroup
from app.main.model.user import sdUser
from app.main.model.customer import sdCustomer
from app.main.model.status_privilege import sdStatusPrivilege
from app.main.service import ret
from app.main.util.geojson_generate import dimming_convert


def generate_status_dimming(cunt):
    remainder = cunt % 5

    if remainder == 1:
        status = 0
        power_status = 1
        dimming = 100
    elif remainder == 2:
        status = 1
        power_status = 1
        dimming = 70
    elif remainder == 3:
        status = 2
        power_status = 1
        dimming = 50
    elif remainder == 4:
        status = 3
        power_status = 0
        dimming = 0
    elif remainder == 0:
        status = 0
        power_status = 1
        dimming = 15
    return status, power_status, dimming


def add_device_geojson_to_db_refjson():
    json = {
        "ret_code": 0,
        "ret_desc": "OK",
        "geojson": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            50.12,
                            50.12
                        ]
                    },
                    "properties": {
                        "id": "9",
                        "name": "9",
                        "display_name": "none",
                        "comment": "null",
                        "status": 0,
                        "power_status": 1,
                        "address": "New Taipei City, Beitou.",
                        "dimming": 15,
                        "dimming_level": 1,
                        "group_name": "testgroup_1",
                        "group_display_name": "test_streetlight"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            50.12,
                            50.12
                        ]
                    },
                    "properties": {
                        "id": "8",
                        "name": "8",
                        "display_name": "none",
                        "comment": "null",
                        "status": 3,
                        "power_status": 0,
                        "address": "New Taipei City, Beitou.",
                        "dimming": 0,
                        "dimming_level": 1,
                        "group_name": "testgroup_1",
                        "group_display_name": "test_streetlight"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            50.12,
                            50.12
                        ]
                    },
                    "properties": {
                        "id": "7",
                        "name": "7",
                        "display_name": "none",
                        "comment": "null",
                        "status": 2,
                        "power_status": 1,
                        "address": "New Taipei City, Beitou.",
                        "dimming": 50,
                        "dimming_level": 3,
                        "group_name": "testgroup_1",
                        "group_display_name": "test_streetlight"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            50.12,
                            50.12
                        ]
                    },
                    "properties": {
                        "id": "6",
                        "name": "6",
                        "display_name": "none",
                        "comment": "null",
                        "status": 1,
                        "power_status": 1,
                        "address": "New Taipei City, Beitou.",
                        "dimming": 70,
                        "dimming_level": 4,
                        "group_name": "testgroup_1",
                        "group_display_name": "test_streetlight"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            50.12,
                            50.12
                        ]
                    },
                    "properties": {
                        "id": "5",
                        "name": "5",
                        "display_name": "none",
                        "comment": "null",
                        "status": 0,
                        "power_status": 1,
                        "address": "New Taipei City, Beitou.",
                        "dimming": 100,
                        "dimming_level": 5,
                        "group_name": "testgroup_1",
                        "group_display_name": "test_streetlight"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            50.12,
                            50.12
                        ]
                    },
                    "properties": {
                        "id": "4",
                        "name": "4",
                        "display_name": "none",
                        "comment": "null",
                        "status": 0,
                        "power_status": 1,
                        "address": "New Taipei City, Beitou.",
                        "dimming": 15,
                        "dimming_level": 1,
                        "group_name": "testgroup_1",
                        "group_display_name": "test_streetlight"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            50.12,
                            50.12
                        ]
                    },
                    "properties": {
                        "id": "3",
                        "name": "3",
                        "display_name": "none",
                        "comment": "null",
                        "status": 3,
                        "power_status": 0,
                        "address": "New Taipei City, Beitou.",
                        "dimming": 0,
                        "dimming_level": 1,
                        "group_name": "testgroup_1",
                        "group_display_name": "test_streetlight"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            50.12,
                            50.12
                        ]
                    },
                    "properties": {
                        "id": "2",
                        "name": "2",
                        "display_name": "none",
                        "comment": "null",
                        "status": 2,
                        "power_status": 1,
                        "address": "New Taipei City, Beitou.",
                        "dimming": 50,
                        "dimming_level": 3,
                        "group_name": "testgroup_1",
                        "group_display_name": "test_streetlight"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            50.12,
                            50.12
                        ]
                    },
                    "properties": {
                        "id": "1",
                        "name": "1",
                        "display_name": "none",
                        "comment": "null",
                        "status": 1,
                        "power_status": 1,
                        "address": "New Taipei City, Beitou.",
                        "dimming": 70,
                        "dimming_level": 4,
                        "group_name": "testgroup_1",
                        "group_display_name": "test_streetlight"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            50.12,
                            50.12
                        ]
                    },
                    "properties": {
                        "id": "0",
                        "name": "0",
                        "display_name": "none",
                        "comment": "null",
                        "status": 0,
                        "power_status": 1,
                        "address": "New Taipei City, Beitou.",
                        "dimming": 100,
                        "dimming_level": 5,
                        "group_name": "testgroup_1",
                        "group_display_name": "test_streetlight"
                    }
                }
            ]
        }
    }
    return json


def add_device_geojson_to_db(max_device):
    ret_json = ret.http_resp(ret.RET_OK)
    user_devices_json = {"type": "FeatureCollection",
                         "features": []}
    for number in range(max_device):
        status, power_status, dimming = generate_status_dimming(number+1)
        each_sample_json = {"type": "Feature",
                            "geometry": {"type": "Point",
                                         "coordinates": [50.12,
                                                         50.12]},
                            "properties": {"id": str(number),
                                           "name": str(number),
                                           "display_name": "none",
                                           "comment": "null",
                                           "status": status,
                                           "power_status": power_status,
                                           "address": "New Taipei City, Beitou.",
                                           "dimming": dimming,
                                           "dimming_level": dimming_convert(dimming),
                                           "group_name": "testgroup_1",
                                           "group_display_name": "test_streetlight"
                                           }}
        user_devices_json["features"].append(each_sample_json)

        testing_device_data = sdDevice(id=each_sample_json["properties"]["id"],
                                       name=each_sample_json["properties"]["name"],
                                       display_name=each_sample_json["properties"]["display_name"],
                                       comment=each_sample_json["properties"]["comment"],
                                       create_time="2019-10-22 11:18:55",
                                       update_time="2019-10-22 11:18:55",
                                       dev_type=1,
                                       cust_id=1,
                                       power_status=power_status,
                                       status=each_sample_json["properties"]["status"],
                                       dimming=each_sample_json["properties"]["dimming"],
                                       wgs_x=each_sample_json["geometry"]["coordinates"][0],
                                       wgs_y=each_sample_json["geometry"]["coordinates"][1],
                                       address=each_sample_json["properties"]["address"],
                                       device_group_id=1
                                       )
        db.session.add(testing_device_data)
    db.session.commit()


def ref_json():
    ret_json = ret.http_resp(ret.RET_OK)
    json = []
    divisor = 10 // 5
    for id in range(3):
        # TAG change str here
        json.append(dict(id=str(id+1),
                         name=f"testname_{id+1}",
                         display_name="奇岩的路燈",
                         comment="測試留言武功蓋世，世界大亂鬥。(){}@#$&*^",
                         status=0,
                         power_status=1,
                         wgs_x=121.8,
                         wgs_y=21.5,
                         address="",
                         dimming=50,
                         dimming_level=3,
                         device_group=dict(id=str(id // divisor + 1),
                                           name=f"testgroup_{id // divisor + 1}",
                                           display_name='test_streetlight',
                                           comment="",
                                           create_time='2019-12-18T00:00:00+08:00',
                                           update_time='2019-12-18T00:00:00+08:00'),
                         controller=dict(id=str(id+1),
                                         name=f"test_controller_{id+1}",
                                         display_name="奇岩的controller",
                                         comment="For Unit Test",
                                         create_time="2019-12-18T00:00:00+08:00",
                                         update_time="2019-12-18T00:00:00+08:00",
                                         model_id=0,
                                         serial_no="BX000{}".format(id+1),
                                         model_name="test_device_model",
                                         model_display_name="Test Device Model"),
                         led=dict(id=str(id+1),
                                  name=f"test_led_{id+1}",
                                  display_name="Test User",
                                  comment="For Unit Test",
                                  create_time="2019-12-18T00:00:00+08:00",
                                  update_time="2019-12-18T00:00:00+08:00",
                                  model_id=0,
                                  serial_no="BX000{}".format(id + 1),
                                  model_name="test_device_model",
                                  model_display_name="Test Device Model")))
    ret_json.update({"devices": json})
    return ret_json


email = {0: "user@ntpc.com",
         1: "user@ntpc.com"}
telephone = {0: "02-12345678",
             1: "02-87654321"}


# insert data for get all / get detail api
def user_insertion():
    for num in range(1, 9):
        if num <= 5:
            customer = "NTPC"
            user_email = email[0]
            user_tel = telephone[0]
        else:
            customer = "TPC"
            user_email = email[1]
            user_tel = telephone[1]
        user_data = sdUser(name=f"user_{num+1}",
                           display_name=f"User_{num+1} ({customer})",
                           password="Test Password",
                           comment="comment here",
                           status=0,
                           cust_id=1,
                           email=user_email,
                           telephone=user_tel)
        db.session.add(user_data)
    db.session.commit()


def admin_user_insertion():
    usergroup = db.session.query(sdUserGroup).filter(sdUserGroup.id == "1").first()
    user1 = sdUser(name="admin",
                   display_name="boss",
                   password="Test Password",
                   comment="comment here",
                   status=0,
                   cust_id=1)
    db.session.add(user1)
    user1.user_groups.append(usergroup)
    user2 = sdUser(name="admin",
                   display_name="vendor admin",
                   password="Test Password",
                   comment="comment here",
                   status=0,
                   cust_id=2)

    user2.user_groups.append(usergroup)

    db.session.add(user2)
    db.session.commit()


def vendor_insertion():
    cust = sdCustomer(name="vendor",
                      display_name="boss",
                      status=0,
                      cust_id=1)
    db.session.add(cust)
    db.session.commit()


def user_getall_ref_json(start, end, mode):
    ret_json = ret.http_resp(ret.RET_OK)
    json = []
    json.append(dict(id="1", name="testuser", display_name="Test User", group=["1"]))
    for num in range(start, end):
        if num <= 6:
            customer = "NTPC"
        else:
            customer = "TPC"
        if mode == 1:
            # TAG change str here
            json.append(dict(id=str(num),
                             name=f"user_{num}",
                             display_name=f"User_{num} ({customer})",
                             group=[]))
        elif mode == 2:
            # TAG change str here
            json.append(dict(id=str(num),
                             name=f"user_{num}",
                             display_name=f"User_{num} ({customer})",
                             group=[],
                             email=email[0],
                             telephone=telephone[0],
                             comment="comment here"))
    ret_json.update({"users": json})
    return ret_json


def usergroup_getall_ref_json():
    ret_json = ret.http_resp(ret.RET_OK)
    json = []
    location = ["三芝", "淡水", "北投"]
    json.append(dict(id="1", name="testuser", display_name="Test User", users=["1"]))
    for num, name in enumerate(location):
        json.append(dict(id=str(num+2),
                         name=name,
                         display_name=f"你好{name}",
                         users=[]))
    ret_json.update({"user_groups": json})
    return ret_json

# generate input dict for add user api


def add_user_generate(start, end):
    user_list = []
    for num in range(start, end):
        if num <= 5:
            customer = "NTPC"
            user_email = email[0]
            user_tel = telephone[0]
        else:
            customer = "TPC"
            user_email = email[1]
            user_tel = telephone[1]
        user_list.append(dict(name=f"user_{num+1}",
                              display_name=f"user_{num+1} ({customer})",
                              comment="comment here",
                              password="AmyAmigo",
                              email=user_email,
                              telephone=user_tel))
    user_dict = {"users": user_list}
    return user_dict


# generate input dict for update user api
def update_user_generate():
    update_list = []
    for num in range(2, 15, 3):
        # TAG change str here
        update_list.append(dict(id=str(num),
                                name=f"user_{num}",
                                display_name="update_name",
                                password="3depacbyn",
                                comment="comment here",
                                email="update@gamil.com",
                                telephone="02-12345678"))
    update = {"users": update_list}
    return update


def expect_getallsummary():
    ref_list = []
    template = [4, 1, 5, 3, 2]
    for num in template:
        ref_list.append(dict(id=str(num),
                             name=f"testgroup_{num}",
                             user_groups=[],
                             schedule_groups=[],
                             device_count=4,
                             warning_count=0,
                             error_count=0,
                             poweroff_count=0))
    getallsummary = {"ret_code": 0, "ret_desc": "OK", "device_groups": ref_list}
    return getallsummary

# generate input dict for add user api


def add_user_groups():
    user_list = []
    name_list = ["三芝", "淡水", "北投"]
    for name in name_list:
        user_list.append(dict(name=name,
                              display_name=f"你好{name}",
                              comment="comment here"))
    user_group_dict = {"user_groups": user_list}
    return user_group_dict


def update_user_groups():
    user_list = []
    name_list = ["新三芝", "新淡水"]
    for new_id, new_name in enumerate(name_list):
        user_list.append(dict(id=str(new_id+1),
                              name=new_name,
                              display_name=f"你好{new_name}",
                              comment="comment here"))
    user_group_dict = {"user_groups": user_list}
    return user_group_dict


def check_device_input():
    json = {
        "devices": [
            {
                "id": "1",
                "name": "testname_2",
                "display_name": "淡水廠的路燈",
                "comment": "這是測試device的小天地，@#$%^&*[]_=+-*",
                "point": {"wgs_x": 27,
                          "wgs_y": 29,
                          "address": "write something"},
                "controller": {"model_name": "test_device_model",
                               "serial_no": "BX0001",
                               "name": "A100"},
                "led": {"model_name": "test_device_model",
                        "serial_no": "BX0001",
                        "name": "A100"}
            }]
    }
    return json


def check_device_refans():
    json = {
        "ret_code": 0,
        "ret_desc": "OK",
        "devices": [
            {
                "id": "1",
                "name": "testname_2",
                "controller": {
                    "name": "A100",
                    "serial_no": "BX0001"
                },
                "led": {
                    "name": "A100",
                    "serial_no": "BX0001"
                },
                "description": {
                    "name": "duplicate"
                }
            }
        ]
    }
    return json


def check_device_group_input():
    json = {
        "device_groups": [
            {
                "id": "2",
                "name": "麥當勞",
                "display_name": "麥當勞抱抱"
            }
        ]
    }
    return json


def check_device_group_refans():
    json = {
        "ret_code": 0,
        "ret_desc": "OK",
        "device_groups": [
            {
                "id": "2",
                "name": "麥當勞",
                "description": {
                    "name": "duplicate"
                }
            }]
    }
    return json


def check_user_input():
    json = {
        "users": [
            {"id": "1",
             "name": "user_2",
             "display_name": "MegaRoyCanon",
             "email": "Roy@yahooooooo.com",
             "telephone": "0912345678",
             "comment": "I come I see I conquer",
             "password": "1234qwer"
             }
        ]
    }
    return json


def check_user_refans():
    json = {
        "ret_code": 0,
        "ret_desc": "OK",
        "users": [
            {
                "id": "1",
                "name": "user_2",
                "description": {
                    "name": "duplicate"
                }
            }
        ]
    }
    return json


def check_user_group_input():
    json = {
        "user_groups": [
            {
                "id": "1",
                "name": "淡水",
                "display_name": "你好淡水",
                "comment": "DS"
            }
        ]
    }

    return json


def check_user_group_refans():
    json = {
        "ret_code": 0,
        "ret_desc": "OK",
        "user_groups": [
            {
                "id": "1",
                "name": "淡水",
                "description": {
                    "name": "duplicate"
                }
            }
        ]
    }
    return json


def check_schedule_input():
    json = {
        "schedule_groups": [
            {
                "id": "1",
                "name": "SG_1",
                "display_name": "GOTY",
                "comment": "leave message",
                "scheme": "24h",
                "incre": "n",
                "schedule_days":
                {
                    "0": {
                        "00:00": 60,
                        "06:00": 0,
                        "17:00": 40,
                        "19:00": 100
                    },
                    "1": {
                        "00:00": 60,
                        "06:00": 0,
                        "17:00": 40,
                        "19:00": 100
                    }
                }
            }
        ]
    }
    return json


def check_schedule_refans():
    json = {
        "ret_code": 0,
        "ret_desc": "OK",
        "schedule_groups": [
            {
                "id": "1",
                "name": "SG_1",
                "description": {
                    "name": "duplicate"
                }
            }
        ]
    }
    return json


def event_getnotice_refans():
    json = {
        "ret_code": 0,
        "ret_desc": "OK",
        "error_count": 2,
        "warning_count": 0,
        "events": [
            {
                "id": "5",
                "device_id": "1",
                "device_name": "testname_1",
                "component": "CONTROLLER",
                "category": "溫度",
                "status": 8,
                "create_time": "2020-02-06T00:00:00+08:00"
            },
            {
                "id": "10",
                "device_id": "2",
                "device_name": "testname_2",
                "component": "CONTROLLER",
                "category": "溫度",
                "status": 8,
                "create_time": "2020-02-06T00:00:00+08:00"
            }
        ]
    }
    return json


def event_get_input():
    json = {
        "events":
        {
            "page": 1,
            "limit": 15,
            "sort_by": "device_id",
            "order_by": "desc",
            "time_interval": ["20200206", "20200208"],
            "filter":
            {
                "ack": [0],
                "status_id": [0],
                "component_id": [0]
            }
        }
    }
    return json


def event_get_refans():
    json = {
        "ret_code": 0,
        "ret_desc": "OK",
        "pagecount": 1,
        "total_found": 2,
        "total_in_db": 10,
        "events": [
            {
                "id": "6",
                "device_id": "2",
                "device_name": "testname_2",
                "device_address": "",
                "component_id": 0,
                "component": "CONTROLLER",
                "category_id": 0,
                "category": "溫度",
                "description": "測試用描述",
                "status": 0,
                "create_time": "2020-02-06T00:00:00+08:00",
                "ack": 0
            },
            {
                "id": "1",
                "device_id": "1",
                "device_name": "testname_1",
                "device_address": "",
                "component_id": 0,
                "component": "CONTROLLER",
                "category_id": 0,
                "category": "溫度",
                "description": "測試用描述",
                "status": 0,
                "create_time": "2020-02-06T00:00:00+08:00",
                "ack": 0
            }
        ]
    }
    return json


def dispatching_getall_ref_ans():
    json = {
        "ret_code": 0,
        "ret_desc": "OK",
        "issues": [
            {
                "id": "1",
                "issue_no": "TX001",
                "issue_status_id": "1",
                "issue_status": "NEW",
                "error_code": "9",
                "error_name": "其他",
                "subject": "TX001 報修單",
                "device_id": "1",
                "device_name": "testname_1",
                "device_address": "",
                "device_status": 0,
                "priority_id": "13",
                "priority_name": "普通",
                "create_time": "2020-01-07T00:00:00+08:00"
            },
            {
                "id": "2",
                "issue_no": "TX002",
                "issue_status_id": "1",
                "issue_status": "NEW",
                "error_code": "9",
                "error_name": "其他",
                "subject": "TX002 報修單",
                "device_id": "1",
                "device_name": "testname_1",
                "device_address": "",
                "device_status": 0,
                "priority_id": "13",
                "priority_name": "普通",
                "create_time": "2020-01-07T00:00:00+08:00"
            },
            {
                "id": "3",
                "issue_no": "TX003",
                "issue_status_id": "1",
                "issue_status": "NEW",
                "error_code": "9",
                "error_name": "其他",
                "subject": "TX003 報修單",
                "device_id": "1",
                "device_name": "testname_1",
                "device_address": "",
                "device_status": 0,
                "priority_id": "13",
                "priority_name": "普通",
                "create_time": "2020-01-07T00:00:00+08:00"
            },
            {
                "id": "4",
                "issue_no": "TX004",
                "issue_status_id": "1",
                "issue_status": "NEW",
                "error_code": "9",
                "error_name": "其他",
                "subject": "TX004 報修單",
                "device_id": "1",
                "device_name": "testname_1",
                "device_address": "",
                "device_status": 0,
                "priority_id": "13",
                "priority_name": "普通",
                "create_time": "2020-01-07T00:00:00+08:00"
            }
        ]
    }
    return json


def dispatching_getdetail_ref_ans():
    json = {
        "ret_code": 0,
        "ret_desc": "OK",
        "issues": [
            {
                "id": "1",
                "issue_no": "TX001",
                "issue_status": "NEW",
                "subject": "TX001 報修單",
                "error_code": "9",
                "error_name": "其他",
                "device_id": "1",
                "device_name": "testname_1",
                "device_address": "",
                "device_status": 0,
                "vendor_id": "1",
                "vendor_name": "Test Customer",
                "assignee_id": "1",
                "assignee_name": "Test User",
                "description": "抱抱抱修單",
                "priority_id": "13",
                "priority_name": "普通",
                "report_from": "1",
                "reporter": "大名",
                "reporter_email": "@123",
                "reporter_mobile": "0931",
                "reporter_phone": "0988",
                "due_day": "2020-01-11",
                "create_time": "2020-01-07T00:00:00+08:00",
                "issue_logs": [
                    {
                        "issue_log_id": "1",
                        "sequence": 1,
                        "subject": "TX001 報修單之log (2)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "1",
                        "status_to": "2",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    },
                    {
                        "issue_log_id": "2",
                        "sequence": 2,
                        "subject": "TX001 報修單之log (3)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "2",
                        "status_to": "3",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    },
                    {
                        "issue_log_id": "3",
                        "sequence": 3,
                        "subject": "TX001 報修單之log (3)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "3",
                        "status_to": "3",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    },
                    {
                        "issue_log_id": "4",
                        "sequence": 4,
                        "subject": "TX001 報修單之log (4)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "3",
                        "status_to": "4",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    },
                    {
                        "issue_log_id": "5",
                        "sequence": 5,
                        "subject": "TX001 報修單之log (5)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "4",
                        "status_to": "5",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    },
                    {
                        "issue_log_id": "6",
                        "sequence": 6,
                        "subject": "TX001 報修單之log (6)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "5",
                        "status_to": "6",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    }
                ]
            },
            {
                "id": "2",
                "issue_no": "TX002",
                "issue_status": "NEW",
                "subject": "TX002 報修單",
                "error_code": "9",
                "error_name": "其他",
                "device_id": "1",
                "device_name": "testname_1",
                "device_address": "",
                "device_status": 0,
                "vendor_id": "0",
                "vendor_name": "Test Customer",
                "assignee_id": "1",
                "assignee_name": "Test User",
                "description": "抱抱抱修單",
                "priority_id": "13",
                "priority_name": "普通",
                "report_from": "1",
                "reporter": "大名",
                "reporter_email": "@123",
                "reporter_mobile": "0931",
                "reporter_phone": "0988",
                "due_day": "2020-01-11",
                "create_time": "2020-01-07T00:00:00+08:00",
                "issue_logs": [
                    {
                        "issue_log_id": "7",
                        "sequence": 1,
                        "subject": "TX002 報修單之log (2)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "1",
                        "status_to": "2",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    },
                    {
                        "issue_log_id": "8",
                        "sequence": 2,
                        "subject": "TX002 報修單之log (3)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "2",
                        "status_to": "3",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    },
                    {
                        "issue_log_id": "9",
                        "sequence": 3,
                        "subject": "TX002 報修單之log (3)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "3",
                        "status_to": "3",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    },
                    {
                        "issue_log_id": "10",
                        "sequence": 4,
                        "subject": "TX002 報修單之log (4)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "3",
                        "status_to": "4",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    },
                    {
                        "issue_log_id": "11",
                        "sequence": 5,
                        "subject": "TX002 報修單之log (5)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "4",
                        "status_to": "5",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    },
                    {
                        "issue_log_id": "12",
                        "sequence": 6,
                        "subject": "TX002 報修單之log (6)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "5",
                        "status_to": "6",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    }
                ]
            },
            {
                "id": "3",
                "issue_no": "TX003",
                "issue_status": "NEW",
                "subject": "TX003 報修單",
                "error_code": "9",
                "error_name": "其他",
                "device_id": "1",
                "device_name": "testname_1",
                "device_address": "",
                "device_status": 0,
                "vendor_id": "1",
                "vendor_name": "Test Customer",
                "assignee_id": "1",
                "assignee_name": "Test User",
                "description": "抱抱抱修單",
                "priority_id": "13",
                "priority_name": "普通",
                "report_from": "1",
                "reporter": "大名",
                "reporter_email": "@123",
                "reporter_mobile": "0931",
                "reporter_phone": "0988",
                "due_day": "2020-01-11",
                "create_time": "2020-01-07T00:00:00+08:00",
                "issue_logs": [
                    {
                        "issue_log_id": "13",
                        "sequence": 1,
                        "subject": "TX003 報修單之log (2)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "1",
                        "status_to": "2",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    },
                    {
                        "issue_log_id": "14",
                        "sequence": 2,
                        "subject": "TX003 報修單之log (3)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "2",
                        "status_to": "3",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    },
                    {
                        "issue_log_id": "15",
                        "sequence": 3,
                        "subject": "TX003 報修單之log (3)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "3",
                        "status_to": "3",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    },
                    {
                        "issue_log_id": "16",
                        "sequence": 4,
                        "subject": "TX003 報修單之log (4)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "3",
                        "status_to": "4",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    },
                    {
                        "issue_log_id": "17",
                        "sequence": 5,
                        "subject": "TX003 報修單之log (5)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "4",
                        "status_to": "5",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    },
                    {
                        "issue_log_id": "18",
                        "sequence": 6,
                        "subject": "TX003 報修單之log (6)",
                        "user_id": "2",
                        "user_name": "anonymous",
                        "description": "issue log",
                        "status_from": "5",
                        "status_to": "6",
                        "create_time": "2020-01-10T00:00:00+08:00"
                    }
                ]
            }
        ]
    }
    return json


def dispatching_update_input():
    json = {
        "action": "3",
        "issues":   [
            {
                "id": "1",
                "assignee_id": "2",
                "description": "狀態轉換",
                "priority_id": "13"
            }
        ]
    }

    return json


def dispatching_getassignee_refans(flag):
    if flag == 0:
        json = {
            "ret_code": 0,
            "ret_desc": "OK",
            "assignee": [
                {
                    "id": "3",
                    "name": "admin",
                    "display_name": "vendor admin",
                    "cust_id": "2",
                    "cust_name": "vendor",
                    "cust_display_name": "boss"
                }
            ]
        }
    elif flag == 1:
        json = {
            "ret_code": 0,
            "ret_desc": "OK",
            "assignee": [
                {
                    "id": "3",
                    "name": "admin",
                    "display_name": "vendor admin",
                    "cust_id": "2",
                    "cust_name": "vendor",
                    "cust_display_name": "boss"
                },
                {
                    "id": "2",
                    "name": "admin",
                    "display_name": "boss",
                    "cust_id": "1",
                    "cust_name": "testcust",
                    "cust_display_name": "Test Customer"
                }
            ]
        }
    return json


def dispatching_getstatus_refans():
    json = {
        "ret_code": 0,
        "ret_desc": "OK",
        "status_privilege": [
            {
                "status_id": 1,
                "status_name": "new"
            },
            {
                "status_id": 3,
                "status_name": "assigned"
            },
            {
                "status_id": 4,
                "status_name": "progress"
            },
            {
                "status_id": 5,
                "status_name": "resolved"
            },
            {
                "status_id": 6,
                "status_name": "closed"
            }
        ]
    }
    return json


def test_auth_add_new_role():
    role = sdRole(
        id=2,
        name="Cust Admin",
        display_name="Cust admin"
    )

    usergroup = sdUserGroup(
        name="b group",
        display_name="Test User"
    )

    status_priv = sdStatusPrivilege(
        role_id=2,
        status_from=3,
        status_to=4,
        cust_id=1
    )
    user = db.session.query(sdUser).filter(sdUser.id == "2").first()
    user.user_groups.clear()
    user.user_groups.append(usergroup)
    usergroup.rel_role_ug.append(role)
    db.session.add(role)
    db.session.add(usergroup)
    db.session.add(status_priv)
    db.session.commit()


def device_group_getallsummary_ref_ans():
    json = {"ret_code": 0,
            "ret_desc": "OK",
            "device_groups":
            [
                {
                    "id": "1",
                    "name": "testgroup_1",
                    "display_name": "test_streetlight",
                    "user_groups": [
                        {
                            "id": "1",
                            "name": "testuser"
                        }
                    ],
                    "schedule_groups": {
                        "id": "1",
                        "name":  "schedule_0"
                    },
                    "device_count": 0,
                    "warning_count": 0,
                    "error_count": 0,
                    "poweroff_count": 0
                },
                {
                    "id": "2",
                    "name": "testgroup_2",
                    "display_name": "test_streetlight",
                    "user_groups": [],
                    "schedule_groups": {
                        "id": "2",
                        "name":  "schedule_1"
                    },
                    "device_count": 0,
                    "warning_count": 0,
                    "error_count": 0,
                    "poweroff_count": 0
                },
                {
                    "id": "3",
                    "name": "testgroup_3",
                    "display_name": "test_streetlight",
                    "user_groups": [],
                    "schedule_groups": {
                        "id": "3",
                        "name":  "schedule_2"
                    },
                    "device_count": 0,
                    "warning_count": 0,
                    "error_count": 0,
                    "poweroff_count": 0
                },
                {
                    "id": "4",
                    "name": "testgroup_4",
                    "display_name": "test_streetlight",
                    "user_groups": [],
                    "schedule_groups": {
                        "id": "4",
                        "name":  "schedule_3"
                    },
                    "device_count": 0,
                    "warning_count": 0,
                    "error_count": 0,
                    "poweroff_count": 0
                },
                {
                    "id": "5",
                    "name": "testgroup_5",
                    "display_name": "test_streetlight",
                    "user_groups": [],
                    "schedule_groups": {
                        "id": "5",
                        "name":  "schedule_4"
                    },
                    "device_count": 0,
                    "warning_count": 0,
                    "error_count": 0,
                    "poweroff_count": 0
                }
            ]}
    return json


def issue_peopleadd_input():
    json = {
        "issues":   [
            {
                "subject": "珍貴的建議",
                "device_id": "1",
                "error_code_display_name": "燈不亮",
                "description": "",
                "reporter": "張中明",
                "reporter_email": "",
                "reporter_mobile": "",
                "reporter_phone": ""
            }
        ]
    }
    return json


def issue_peopleadd_refans():
    json = {
        "ret_code": 0,
        "ret_desc": "OK",
        "issues": [
            {
                    "id": "1",
                    "issue_no": "NTPC-20200421-00001",
                    "subject": "珍貴的建議"
            }
        ]
    }
    return json
