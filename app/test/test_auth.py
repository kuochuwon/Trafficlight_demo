import json
import unittest

from flask_api import status
from flask_jwt_extended import get_raw_jwt

from app.main import db
from app.main.model.issue import sdIssue
from app.main.log import logger
from app.main.model.blacklist import sdBlacklistToken
from app.main.service import ret
from app.test.base import BaseTestCase
from app.test.stubs.data import FakeDataCreation

from app.test.stubs.pseudo_device_creating import (dispatching_update_input,
                                                   admin_user_insertion,
                                                   vendor_insertion,
                                                   user_getall_ref_json,
                                                   user_insertion,
                                                   test_auth_add_new_role)


class TestAuth(BaseTestCase):

    def test_login_succ(self):
        resp = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({"custname": self.cust_name,
                             "username": self.user_name,
                             "password": self.user_pass}),
            content_type="application/json"
        )
        data = json.loads(resp.data.decode())
        jwt_token = data.get("token")

        self.assert200(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("ret_code"), ret.RET_OK)
        self.assertTrue(jwt_token is not None)

    def test_login_bad_case(self):
        # 400 bad request, (2001) Missing customer name, user name, or password
        resp = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({"custname": "",
                             "username": "",
                             "password": ""}),
            content_type="application/json"
        )
        data = json.loads(resp.data.decode())

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data.get("ret_code"), ret.RET_AUTH_MISSING)

        # 401, (2002) Invalid customer name
        resp = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({"custname": "2",
                             "username": self.user_name,
                             "password": self.user_pass}),
            content_type="application/json"
        )
        data = json.loads(resp.data.decode())

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(data.get("ret_code"), ret.RET_AUTH_NO_CUST)

        # 401, (2003) Invalid user name
        resp = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({"custname": self.cust_name,
                             "username": "123",
                             "password": self.user_pass}),
            content_type="application/json"
        )

        data = json.loads(resp.data.decode())

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(data.get("ret_code"), ret.RET_AUTH_NO_USER)

        # 401, (2004) Invalid user name or password
        resp = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({"custname": self.cust_name,
                             "username": self.user_name,
                             "password": "123"}),
            content_type="application/json"
        )

        data = json.loads(resp.data.decode())

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(data.get("ret_code"), ret.RET_AUTH_WRONG_PASS)

    def test_logout(self):
        resp = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({"custname": self.cust_name,
                             "username": self.user_name,
                             "password": self.user_pass}),
            content_type="application/json"
        )
        data = json.loads(resp.data.decode())
        token_hex = data.get("token")["refresh_token"]
        resp = self.client.get("/api/v1/auth/logout",
                               headers={"Authorization": f"Bearer {token_hex}"})
        self.assertEqual(resp.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(data.get("ret_code"),
                         ret.RET_OK)

        jti = get_raw_jwt()["jti"]
        token_saved = sdBlacklistToken.query.filter(sdBlacklistToken.token == jti).first()
        self.assertTrue(token_saved)

    def test_logout_bad_case(self):
        resp = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({"custname": self.cust_name,
                             "username": self.user_name,
                             "password": self.user_pass}),
            content_type="application/json"
        )
        data = json.loads(resp.data.decode())
        token_hex = data.get("token")["refresh_token"]
        resp = self.client.get("/api/v1/auth/logout",
                               headers={"Authorization": f"Bearer {token_hex}"})

        # Throw again to validate token was revoke
        resp = self.client.get("/api/v1/auth/logout",
                               headers={"Authorization": f"Bearer {token_hex}"})

        data = json.loads(resp.data.decode())
        self.assert401(resp)
        self.assertEqual(data.get("ret_desc"), "Token has expired")

    def test_get_access(self):
        resp = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({"custname": self.cust_name,
                             "username": self.user_name,
                             "password": self.user_pass}),
            content_type="application/json"
        )

        data = json.loads(resp.data.decode())

        resp = self.client.post("/api/v1/auth/refresh",
                                headers={"Authorization": f"Bearer {data['token'].get('refresh_token')}"})

        data = json.loads(resp.data.decode())
        jwt_token = data.get("access_token")
        self.assert200(resp)
        self.assertTrue(jwt_token is not None)

    def test_expire_exception(self):
        resp = self.client.post("/api/v1/auth/refresh",
                                headers={"Authorization":
                                         "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzUy"
                                         "NzE5ODMsIm5iZiI6MTU3NTI3MTk4MywianRpIjoiMGM0YmM3YzEtZTg5Yy00Z"
                                         "DM2LTk4NWUtNmEyMDI5NDdkZTYwIiwiZXhwIjoxNTc1MjcyMDEzLCJpZGVudG"
                                         "l0eSI6IntcInVzZXJuYW1lXCI6IFwidGVzdFwiLCBcImN1c3RfaWRcIjogXCJ"
                                         "Nb21vXCIsIFwidXNlcl9pZFwiOiBcIlJlZWJhXCJ9IiwiZnJlc2giOmZhbHNl"
                                         "LCJ0eXBlIjoiYWNjZXNzIn0.g1-YNKGbB2g5Bw0w7i081cingYWJYJh4GgZH"
                                         "gpxt9UA"})

        data = json.loads(resp.data.decode())
        self.assert401(resp)
        self.assertEqual(data, {"ret_code": 2005, "ret_desc": "Token has expired"})

    def test_missing_header(self):
        resp = self.client.post("/api/v1/auth/refresh")
        data = json.loads(resp.data.decode())
        self.assert401(resp)
        self.assertEqual(data, {"ret_code": 2006, "ret_desc": "Missing token"})

    def test_user_access_authorization(self):
        # take account as example
        user_insertion()
        token = self.login()
        resp = self.client.get("/api/v1/account/getall",
                               headers={"Authorization": f"Bearer {token}"})
        logger.debug(resp.status)
        data = json.loads(resp.data.decode())
        ref_json = user_getall_ref_json(2, 10, 1)
        self.assert200(resp)
        self.assertEqual(data, ref_json)

    def test_user_access_authorization_bad(self):
        # take account as example
        user_insertion()
        token = self.login("testcust", "user_2")
        resp = self.client.get("/api/v1/account/getall",
                               headers={"Authorization": f"Bearer {token}"})
        logger.debug(resp.status)
        data = json.loads(resp.data.decode())
        self.assert401(resp)
        self.assertEqual(data, {"ret_code": 2008, "ret_desc": "API access authorization fail"})

    def test_status_privilege_authorization(self):
        # take dispatching update as example
        FakeDataCreation().insert_code_spec()
        vendor_insertion()
        admin_user_insertion()
        FakeDataCreation().user_for_issue().insert_device_group(1, 0).insert_device(1)\
            .insert_issue_cust1(5).insert_issue_log()

        token = self.login("testcust", "admin")
        update_accept = dispatching_update_input()
        resp = self.client.put("/api/v1/issue/update",
                               data=json.dumps(update_accept),
                               content_type="application/json",
                               headers={"Authorization": f"Bearer {token}"})

        stmt = db.select([sdIssue.status_id]).where(sdIssue.id == 1)
        new_status = db.session.execute(stmt).fetchone()[0]
        self.assert200(resp)
        self.assertEqual(new_status, 3)

    def test_status_privilege_authorization_bad(self):
        # take account as example
        FakeDataCreation().insert_code_spec()
        vendor_insertion()
        admin_user_insertion()
        FakeDataCreation().user_for_issue().insert_device_group(1, 0).insert_device(1)\
            .insert_issue_cust1(5).insert_issue_log()
        test_auth_add_new_role()

        # TODO this is example of user_name != "admin"
        token = self.login()
        update_accept = dispatching_update_input()
        resp = self.client.put("/api/v1/issue/update",
                               data=json.dumps(update_accept),
                               content_type="application/json",
                               headers={"Authorization": f"Bearer {token}"})
        logger.debug(resp.status)
        data = json.loads(resp.data.decode())
        self.assert401(resp)
        self.assertEqual(data, {"ret_code": 2003,
                                "ret_desc": "Invalid user name",
                                "ret_hint": "user_name received: testuser"})


if __name__ == "__main__":
    unittest.main()
