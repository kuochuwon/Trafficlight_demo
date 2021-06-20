import json

from app.main import db
from app.main.model.device_group import sdDeviceGroup
from app.main.model.user_group import rel_u_ug, sdUserGroup
from app.main.service import ret
from app.test.base import BaseTestCase
from app.test.stubs.data import FakeDataCreation
from app.test.stubs.pseudo_device_creating import (add_user_generate,
                                                   add_user_groups,
                                                   update_user_groups,
                                                   usergroup_getall_ref_json)


class TestAccountGroupApi(BaseTestCase):
    def test_account_group_getall(self):
        input_data = add_user_groups()
        expect = usergroup_getall_ref_json()
        token = self.login()
        resp = self.client.post("api/v1/account/group/add",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})

        resp = self.client.get("api/v1/account/group/getall",
                               headers={"Authorization": f"Bearer {token}"})
        data = json.loads(resp.data.decode())
        expect = json.dumps(expect, indent=4)
        data = json.dumps(data, indent=4)
        self.assertEqual(data, expect)

    def test_account_group_add(self):
        input_data = add_user_groups()
        token = self.login()
        resp = self.client.post("api/v1/account/group/add",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(json.loads(resp.data.decode()),
                         {"ret_code": 0, "ret_desc": "OK", "users": [{"id": "2", "name": "三芝"},
                                                                     {"id": "3", "name": "淡水"},
                                                                     {"id": "4", "name": "北投"}]})

    def test_account_group_delete(self):
        input_data = add_user_groups()
        token = self.login()
        resp = self.client.post("api/v1/account/group/add",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})

        FakeDataCreation().insert_device_group(5, 0)
        my_user_group = db.session.query(sdUserGroup).filter(sdUserGroup.id.in_(["1", "2"])).all()
        rel_list = []
        for num in range(1, 6):
            query_obj = db.session.query(sdDeviceGroup).filter(sdDeviceGroup.id == num).first()
            rel_list.append(query_obj)
        for user_group in my_user_group:
            user_group.rel_dg_ug = rel_list
        db.session.commit()

        input_list = dict(user_groups=["1", "2"])
        resp = self.client.delete("api/v1/account/group/delete",
                                  data=json.dumps(input_list),
                                  content_type="application/json",
                                  headers={"Authorization": f"Bearer {token}"})
        self.assert200(resp)
        self.assertEqual(json.loads(resp.data.decode()),
                         {"ret_code": 0, "ret_desc": "OK"})

    def test_account_group_update(self):
        # TAG add into DB
        input_data = add_user_groups()
        token = self.login()
        resp = self.client.post("api/v1/account/group/add",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})
        # TAG update DB
        update_data = update_user_groups()
        resp = self.client.put("api/v1/account/group/update",
                               data=json.dumps(update_data),
                               content_type="application/json",
                               headers={"Authorization": f"Bearer {token}"})

        data = json.loads(resp.data.decode())

        self.assert200(resp)
        self.assertEqual(data, {'ret_code': 0, 'ret_desc': 'OK'})

        stmt = db.select([sdUserGroup.id])
        db_changed = [i[0] for i in db.session.execute(stmt).fetchall()]
        self.assertEqual(db_changed, [3, 4, 1, 2])

    def test_account_group_join(self):
        # TAG add usergroup
        input_data = add_user_groups()
        token = self.login()
        resp = self.client.post("api/v1/account/group/add",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})

        # TAG add users
        input_data = add_user_generate(1, 6)
        resp = self.client.post("api/v1/account/add",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})

        # TAG join users
        input_data = {"users": ["1", "2", "3"]}

        resp = self.client.put("api/v1/account/group/2/join",
                               data=json.dumps(input_data),
                               content_type="application/json",
                               headers={"Authorization": f"Bearer {token}"})
        data = json.loads(resp.data.decode())
        expect = ret.http_resp(ret.RET_OK)
        self.assert200(resp)
        self.assertEqual(data, expect)
        query = db.session.query(rel_u_ug).filter(rel_u_ug.c.user_group_id == 2).all()
        self.assertTrue([(1, 2), (2, 2), (3, 2)] == query)

    def test_account_group_leave(self):
        # TAG add usergroup
        # FakeDataCreation().insert_device_group(5).insert_device(20)
        input_data = add_user_groups()
        token = self.login()
        resp = self.client.post("api/v1/account/group/add",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})

        # TAG add users
        input_data = add_user_generate(1, 6)
        resp = self.client.post("api/v1/account/add",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})

        # TAG join users
        input_data = {"users": ["1", "2", "3"]}

        resp = self.client.put("api/v1/account/group/2/join",
                               data=json.dumps(input_data),
                               content_type="application/json",
                               headers={"Authorization": f"Bearer {token}"})

        # TAG leave users
        input_data = {"users": ["3"]}

        resp = self.client.put("api/v1/account/group/2/leave",
                               data=json.dumps(input_data),
                               content_type="application/json",
                               headers={"Authorization": f"Bearer {token}"})

        data = json.loads(resp.data.decode())
        expect = ret.http_resp(ret.RET_OK)
        self.assert200(resp)
        self.assertEqual(data, expect)
        query = db.session.query(rel_u_ug).filter(rel_u_ug.c.user_group_id == 2).all()
        self.assertTrue([(1, 2), (2, 2)] == query)
