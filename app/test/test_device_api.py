import unittest
import json
from sqlalchemy import func
from app.main.log import logger
from app.main.service import ret
from app.main import db
from app.main.model.device import sdDevice
from app.main.model.controller import sdController
from app.main.model.led import sdLed
from app.test.base import BaseTestCase
from app.test.stubs.data import compose_input_for_device, FakeDataCreation
from app.test.stubs.pseudo_device_creating import add_device_geojson_to_db, ref_json, add_device_geojson_to_db_refjson


class TestDevice(BaseTestCase):
    def test_getdetail_device(self):
        FakeDataCreation().insert_device_group(5, 0).insert_device(10)
        getdetail_data = {"devices": ["1", "2", "3"]}
        token = self.login()
        resp = self.client.post("/api/v1/device/getdetail",
                                data=json.dumps(getdetail_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})
        logger.debug("get detail Reponse " + resp.status)
        text = resp.data.decode()
        json_text = json.loads(text)
        json_text = json.dumps(json_text, indent=4)
        ref_ans = ref_json()
        ref_ans = json.dumps(ref_ans, indent=4)
        self.assertEqual(json_text, ref_ans)

    def test_getall_geojson(self):
        FakeDataCreation().insert_device_group(1, 0)
        add_device_geojson_to_db(self.max_device)
        ref_json = add_device_geojson_to_db_refjson()
        token = self.login()
        resp = self.client.post("/api/v1/device/getall",
                                data=json.dumps({"user": self.user_name,
                                                 "max_device": self.max_device}),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})
        json_text = json.loads(resp.data.decode())  # for comparing with reference answer

        ref_json = json.dumps(ref_json, indent=4)
        json_text = json.dumps(json_text, indent=4)
        self.assertEqual(json_text, ref_json)

    def test_delete_device(self):
        FakeDataCreation().insert_device_group(2, 0).insert_device(8)

        delete_data = {"devices": ["1", "2", "3"]}
        token = self.login()
        resp = self.client.delete("/api/v1/device/delete",
                                  data=json.dumps(delete_data),
                                  content_type="application/json",
                                  headers={"Authorization": f"Bearer {token}"})
        logger.debug("Delete Reponse " + resp.status)
        data = json.loads(resp.data.decode())
        expect = ret.http_resp(ret.RET_OK)
        stmt = db.select([sdDevice.id])
        db_changed = [i[0] for i in db.session.execute(stmt).fetchall()]
        self.assert200(resp)
        self.assertEqual(data, expect)
        # test db changed
        self.assertEqual(db_changed, [4, 5, 6, 7, 8])

    def test_add_device(self):
        expect = {'ret_code': 0, 'ret_desc': 'OK', 'devices': [{'id': "1", 'name': 'testname_1'},
                                                               {'id': "2", 'name': 'testname_2'},
                                                               {'id': "3", 'name': 'testname_3'}]}
        FakeDataCreation().insert_device_model(2)
        input_data = compose_input_for_device(3)

        token = self.login()
        resp = self.client.post("/api/v1/device/add",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})

        self.assertEqual(json.loads(resp.data.decode()), expect)

        # add newcase for testing miss led or controller
        input_data = {"devices": [dict(id=f"{10}",
                                       name=f"testname_{10}",
                                       display_name="淡水廠的路燈",
                                       comment="這是測試device的小天地，@#$%^&*[]_=+-*",
                                       wgs_x=27.0,
                                       wgs_y=29.0,
                                       address="write something")]}

        token = self.login()
        resp = self.client.post("/api/v1/device/add",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})

        expect = {'ret_code': 0, 'ret_desc': 'OK', 'devices': [{'id': '4', 'name': 'testname_10'}]}
        self.assertEqual(json.loads(resp.data.decode()), expect)

    def test_update_device(self):
        FakeDataCreation().insert_device_group(1, 0).insert_device(5)

        # There are 3 device in db, and I put 5 device into update
        # So 3 device in db will be changed, and 2 device will be add
        input_data = compose_input_for_device(5)

        token = self.login()
        resp = self.client.put("/api/v1/device/update",
                               data=json.dumps(input_data),
                               content_type="application/json",
                               headers={"Authorization": f"Bearer {token}"})

        data = json.loads(resp.data.decode())

        self.assert200(resp)
        self.assertEqual(data, {'ret_code': 0, 'ret_desc': 'OK'})

        stmt = db.select([sdDevice.id]).where(sdDevice.display_name == "淡水廠的路燈")
        db_changed = [i[0] for i in db.session.execute(stmt).fetchall()]
        stmt = db.select([sdDevice.wgs_x, sdDevice.wgs_y, sdDevice.address])
        point = [tuple(i) for i in db.session.execute(stmt).fetchall()]

        # Total 5 leds and 5 controllers
        db_led = db.session.execute(db.select([func.count(sdLed.id)])).fetchone()[0]
        db_controller = db.session.execute(db.select([func.count(sdController.id)])).fetchone()[0]

        self.assertEqual(db_changed, [1, 2, 3, 4, 5])
        self.assertEqual(set(point), {(27.0, 29.0, 'write something')})
        self.assertEqual(db_led, 5)
        self.assertEqual(db_controller, 5)

        # change only device
        input_data = {"devices": [dict(id=f"{1}",
                                       name=f"testname_{1}",
                                       display_name="安泰路燈",
                                       comment="安泰的路燈好棒棒@#$%^&*[]_=+-*",
                                       wgs_x=23.5,
                                       wgs_y=77.2,
                                       address="紅樹林")]}

        token = self.login()
        resp = self.client.put("/api/v1/device/update",
                               data=json.dumps(input_data),
                               content_type="application/json",
                               headers={"Authorization": f"Bearer {token}"})

        expect = {'ret_code': 0, 'ret_desc': 'OK'}
        self.assertEqual(json.loads(resp.data.decode()), expect)

        input_data = {"devices": [dict(id=f"{1}",
                                       name=f"testname_{1}",
                                       display_name="安泰路燈",
                                       comment="安泰的路燈好棒棒@#$%^&*[]_=+-*",
                                       wgs_x=23.5,
                                       wgs_y=77.2,
                                       address="紅樹林",
                                       controller={"model_name": "GPD002-000GT",
                                                   "name": "ABCCEDFG",
                                                   "display_name": "2019/12/19",
                                                   "comment": "controller xorowo",
                                                   "serial_no": "BX0007"}
                                       )]}

        token = self.login()
        resp = self.client.put("/api/v1/device/update",
                               data=json.dumps(input_data),
                               content_type="application/json",
                               headers={"Authorization": f"Bearer {token}"})

        expect = {'ret_code': 0, 'ret_desc': 'OK'}
        self.assertEqual(json.loads(resp.data.decode()), expect)

        input_data = {"devices": [dict(id=f"{1}",
                                       name=f"testname_{1}",
                                       display_name="安泰路燈",
                                       comment="安泰的路燈好棒棒@#$%^&*[]_=+-*",
                                       wgs_x=23.5,
                                       wgs_y=77.2,
                                       address="紅樹林",
                                       led={"model_name": "LM1109-I1FGT",
                                            "name": "5698",
                                            "display_name": "2019/12/19",
                                            "comment": "pluha",
                                            "serial_no": "A7kjL"}
                                       )]}

        token = self.login()
        resp = self.client.put("/api/v1/device/update",
                               data=json.dumps(input_data),
                               content_type="application/json",
                               headers={"Authorization": f"Bearer {token}"})

        expect = {'ret_code': 0, 'ret_desc': 'OK'}
        self.assertEqual(json.loads(resp.data.decode()), expect)


if __name__ == "__main__":
    unittest.main()
