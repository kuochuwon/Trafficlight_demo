import json
from app.test.base import BaseTestCase
from app.main import db
from app.main.service import ret
from app.main.model.user import sdUser
from app.main.log import logger
from app.test.stubs.pseudo_device_creating import user_getall_ref_json, user_insertion, add_user_generate
from app.test.stubs.pseudo_device_creating import update_user_generate


class TestAccountApi(BaseTestCase):
    def test_account_getall(self):
        user_insertion()
        token = self.login()
        resp = self.client.get("/api/v1/account/getall",
                               headers={"Authorization": f"Bearer {token}"})
        logger.debug(resp.status)
        data = json.loads(resp.data.decode())
        ref_json = user_getall_ref_json(2, 10, 1)
        self.assert200(resp)
        self.assertEqual(data, ref_json)

    def test_account_getdetail(self):
        user_insertion()
        input_data = dict(users=["2", "3", "4"])
        token = self.login()
        resp = self.client.post("/api/v1/account/getdetail",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})
        logger.debug(resp.status)
        data = json.loads(resp.data.decode())
        ref_json = user_getall_ref_json(2, 5, 2)
        ref_json["users"].pop(0)
        self.assert200(resp)
        self.assertEqual(data, ref_json)

    def test_account_add(self):
        input_data = add_user_generate(1, 6)
        token = self.login()
        resp = self.client.post("api/v1/account/add",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})
        self.assert200(resp)
        self.assertEqual(json.loads(resp.data.decode()),
                         {"ret_code": 0, "ret_desc": "OK", "users": [{"id": "2", "name": "user_2"},
                                                                     {"id": "3", "name": "user_3"},
                                                                     {"id": "4", "name": "user_4"},
                                                                     {"id": "5", "name": "user_5"},
                                                                     {"id": "6", "name": "user_6"}]})

    def test_account_delete(self):
        user_insertion()

        delete_data = {"users": ["2", "3", "4"]}
        token = self.login()
        resp = self.client.delete("/api/v1/account/delete",
                                  data=json.dumps(delete_data),
                                  content_type="application/json",
                                  headers={"Authorization": f"Bearer {token}"})

        logger.debug("Delete Reponse " + resp.status)
        data = json.loads(resp.data.decode())

        expect = ret.http_resp(ret.RET_OK)

        stmt = db.select([sdUser.id])

        db_changed = [i[0] for i in db.session.execute(stmt).fetchall()]

        self.assert200(resp)
        self.assertEqual(data, expect)

        # test db changed
        self.assertEqual(db_changed, [1, 5, 6, 7, 8, 9])

    def test_account_update(self):
        # There are 9 users in db (id: 1 ~ 9), and 5 updated users
        # updated users id: 2,5,8 ; added users id: 10, 11
        user_insertion()
        input_data = update_user_generate()
        token = self.login()
        resp = self.client.put("api/v1/account/update",
                               data=json.dumps(input_data),
                               content_type="application/json",
                               headers={"Authorization": f"Bearer {token}"})

        data = json.loads(resp.data.decode())

        self.assert200(resp)
        self.assertEqual(data, {'ret_code': 0, 'ret_desc': 'OK'})

        stmt = db.select([sdUser.id]).where(sdUser.display_name == "update_name")
        db_changed = [i[0] for i in db.session.execute(stmt).fetchall()]
        self.assertEqual(db_changed, [2, 5, 8, 10, 11])
