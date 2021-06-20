import json
import os
from sqlalchemy import func
from app.test.base import BaseTestCase
from app.test.stubs.data import ExpectResponse, FakeDataCreation
from app.main.log import logger
from app.main.service import ret
from app.main import db
from app.main.model.device import sdDevice
from app.main.model.device_group import sdDeviceGroup
from app.main.model.user_group import rel_dg_ug, sdUserGroup
from app.test.stubs.pseudo_device_creating import add_user_groups, device_group_getallsummary_ref_ans


file_dir = os.path.dirname(__file__)


class TestDeviceGroupApi(BaseTestCase):

    def test_group_getallsummary(self):
        # FakeDataCreation().insert_device_group(5, 0).insert_device(20)
        FakeDataCreation().insert_schedule_group(6).insert_schedule_item().insert_device_group(5, 0)
        device_group = db.session.query(sdDeviceGroup).filter(sdDeviceGroup.id == 1).first()
        user_group = db.session.query(sdUserGroup).filter(sdUserGroup.id == 1).first()
        user_group.rel_dg_ug.append(device_group)
        db.session.commit()
        # device_group.user_groups.append(user_group)
        token = self.login()
        resp = self.client.get("/api/v1/device/group/getallsummary", headers={"Authorization": f"Bearer {token}"})

        logger.debug(resp.status)
        # If not 200, this will crash
        rawdata = json.loads(resp.data.decode())
        # dg = rawdata.get("device_groups")
        sorted_data = sorted(rawdata.get("device_groups"), key=lambda issue: issue.get("id"))
        rawdata["device_groups"] = sorted_data
        data = json.dumps(rawdata, indent=4)
        expect = device_group_getallsummary_ref_ans()
        expect = json.dumps(expect, indent=4)
        self.assert200(resp)
        self.assertEqual(data, expect)

    def test_group_getall(self):
        FakeDataCreation().insert_device_group(5, 0).insert_device(20)
        expect = ExpectResponse().compose_response_body().count(5, 20).group_id().name().display_name().user_groups()\
            .devices().response()

        token = self.login()
        resp = self.client.get("/api/v1/device/group/getall", headers={"Authorization": f"Bearer {token}"})

        logger.debug(resp.status)
        # If not 200, this will crash
        data = json.loads(resp.data.decode())
        # Expect response is HTTP status 200
        self.assert200(resp)
        self.assertEqual(data, expect)

    def test_group_getdetail(self):
        FakeDataCreation().insert_schedule_group(2).insert_schedule_item().insert_device_group(5, 5).insert_device(20)

        token = self.login()
        input_data = {"device_groups": ["1", "2"]}
        resp = self.client.post("/api/v1/device/group/getdetail",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})

        logger.debug(resp.status)
        # If not 200, this will crash
        data = json.loads(resp.data.decode())

        with open(file_dir + r"\stubs\device_group_getdetail.json", "r", encoding="utf-8") as reader:
            expect = json.loads(reader.read())
        # Expect response is HTTP status 200
        self.assert200(resp)
        self.assertEqual(data, expect)

    def test_group_add(self):
        sample_data = [("麥當勞", "雞塊旁的路燈"), ("肯德基", "雞米花上的路燈"), ("漢堡王", "小華堡裡的路燈")]
        input_data = {"device_groups": [dict(name=name[0],
                                             display_name=name[1]) for count, name in zip(range(3), sample_data)]}

        token = self.login()
        resp = self.client.post("/api/v1/device/group/add",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})

        data = json.loads(resp.data.decode())

        expect = ExpectResponse().compose_response_body().count(3, 0).group_id().name().response()

        expect['device_groups'] = [dict(id=str(count+1), name=name[0])
                                   for count, name in zip(range(3), sample_data)]

        self.assertStatus(resp, 201, message=None)
        self.assertEqual(data, expect)

        stmt = db.select([sdDeviceGroup.name, sdDeviceGroup.display_name]).where(sdDeviceGroup.cust_id == 1)

        db_changed = [dict(name=name, display_name=display_name) for name, display_name in
                      db.session.execute(stmt).fetchall()]

        # test db changed
        self.assertEqual(len(db_changed), 3)
        self.assertEqual(db_changed, input_data['device_groups'])

    def test_group_join(self):
        FakeDataCreation().insert_device_group(5, 0).insert_device(20)

        input_data = {"devices": ["17", "18", "19"]}

        token = self.login()
        resp = self.client.put("/api/v1/device/group/3/join",
                               data=json.dumps(input_data),
                               content_type="application/json",
                               headers={"Authorization": f"Bearer {token}"})

        logger.debug("Join Group {} {}".format(resp.status, input_data['devices']))

        data = json.loads(resp.data.decode())

        expect = ret.http_resp(ret.RET_OK)

        self.assert200(resp)
        self.assertEqual(data, expect)

        query = db.select([sdDevice.id]).where(sdDevice.device_group_id == 3)
        devices = [device_id[0] for device_id in db.session.execute(query).fetchall()]
        self.assertTrue([9, 10, 11, 12, 17, 18, 19] == devices)

    def test_ug_join_dg(self):
        # TAG add device group
        FakeDataCreation().insert_device_group(5, 0).insert_device(20)

        # TAG add usergroup
        input_data = add_user_groups()
        token = self.login()
        resp = self.client.post("api/v1/account/group/add",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})

        input_data = {"user_groups": ["2", "3"]}

        resp = self.client.put("/api/v1/device/group/2/join_ug",
                               data=json.dumps(input_data),
                               content_type="application/json",
                               headers={"Authorization": f"Bearer {token}"})
        data = json.loads(resp.data.decode())

        expect = ret.http_resp(ret.RET_OK)

        self.assert200(resp)
        self.assertEqual(data, expect)
        query = db.session.query(rel_dg_ug).filter(rel_dg_ug.c.device_group_id == 2).all()
        self.assertTrue([(2, 2), (2, 3)] == query)

    def test_ug_leave_dg(self):
        # TAG add device group
        FakeDataCreation().insert_device_group(5, 0).insert_device(20)

        # TAG add usergroup
        input_data = add_user_groups()
        token = self.login()
        resp = self.client.post("api/v1/account/group/add",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})

        # TAG join usergroup
        input_data = {"user_groups": ["2", "3"]}
        resp = self.client.put("/api/v1/device/group/2/join_ug",
                               data=json.dumps(input_data),
                               content_type="application/json",
                               headers={"Authorization": f"Bearer {token}"})

        # TAG leave usergroup
        input_data = {"user_groups": ["2"]}
        resp = self.client.put("/api/v1/device/group/2/leave_ug",
                               data=json.dumps(input_data),
                               content_type="application/json",
                               headers={"Authorization": f"Bearer {token}"})

        data = json.loads(resp.data.decode())

        expect = ret.http_resp(ret.RET_OK)

        self.assert200(resp)
        self.assertEqual(data, expect)
        query = db.session.query(rel_dg_ug).filter(rel_dg_ug.c.device_group_id == 2).all()
        self.assertTrue([(2, 3)] == query)

    def test_group_update(self):
        FakeDataCreation().insert_device_group(5, 0)

        rename_data = {"device_groups": [dict(id=str(count), name=f"{name}", display_name="McDonald")
                                         for count, name in zip(range(1, 4), ["hungry", "milk tea", "buddha tea"])]}

        token = self.login()
        resp = self.client.put("/api/v1/device/group/update",
                               data=json.dumps(rename_data),
                               content_type="application/json",
                               headers={"Authorization": f"Bearer {token}"})

        logger.debug("Rename Response " + resp.status)
        data = json.loads(resp.data.decode())

        query = db.select([func.count()]).where(sdDeviceGroup.display_name == 'McDonald')
        db_changed = db.session.execute(query).fetchone()[0]

        expect = ret.http_resp(ret.RET_OK)

        self.assert200(resp)
        self.assertEqual(data, expect)

        # test db changed
        self.assertEqual(db_changed, 3)

    def test_group_delete(self):
        FakeDataCreation().insert_device_group(5, 0).insert_device(20)

        delete_data = {"device_groups": ["1", "2", "3"]}

        token = self.login()

        resp = self.client.delete("/api/v1/device/group/delete",
                                  data=json.dumps(delete_data),
                                  content_type="application/json",
                                  headers={"Authorization": f"Bearer {token}"})

        logger.debug("Delete Reponse " + resp.status)
        data = json.loads(resp.data.decode())

        expect = ret.http_resp(ret.RET_OK)

        stmt = db.select([sdDeviceGroup.id])

        db_changed = [i[0] for i in db.session.execute(stmt).fetchall()]

        self.assert200(resp)
        self.assertEqual(data, expect)

        # test db changed
        self.assertEqual(db_changed, [4, 5])
