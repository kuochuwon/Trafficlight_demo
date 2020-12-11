import json
import os

from flask_testing import TestCase
from app.main import db
from app.main.model.user import sdUser
from app.main.model.customer import sdCustomer
from app.main.model.user_group import sdUserGroup
from app.main.model.device_model import sdDeviceModel
from app.main.model.roles import sdRole
from app.main.model.privileges import sdPrivilege
from app.main.model.status_privilege import sdStatusPrivilege
from manage import app

file_dir = os.path.dirname(__file__)


class BaseTestCase(TestCase):
    """ Base Tests """

    cust_name = "testcust"
    user_name = "testuser"
    user_pass = "Test Password"
    max_device = 10
    token = None

    def create_privilege(self):
        with open(file_dir + r"\stubs\role_privilege.json", "r", encoding="utf-8") as reader:
            expect = json.loads(reader.read())
        for k, v in expect.items():
            for routes in v:
                priv = sdPrivilege(
                    role_id=k,
                    api_route=routes
                )
                db.session.add(priv)

        with open(file_dir + r"\stubs\status_privilege.json", "r", encoding="utf-8") as reader:
            expect = json.loads(reader.read())
        for k, v in expect.items():
            for column in v:
                s_priv = sdStatusPrivilege(
                    role_id=k,
                    status_from=column[0],
                    status_to=column[1],
                    cust_id=column[2]
                )
                db.session.add(s_priv)

        db.session.commit()

    def create_cust_user_user_group(self):
        cust = sdCustomer(
            name=self.cust_name,
            display_name="Test Customer",
            comment="For Unit Test"
        )
        user = sdUser(
            name=self.user_name,
            display_name="Test User",
            password=self.user_pass,
            comment="For Unit Test"
        )
        user_group = sdUserGroup(
            name=self.user_name,
            display_name="Test User"
        )

        role = sdRole(
            name="system_admin",
            display_name="System_Admin"
        )

        cust.users.append(user)
        # add cust_id to usergroup
        cust.user_groups.append(user_group)
        # add u_ug table
        user.user_groups.append(user_group)
        # add role_ug table
        user_group.rel_role_ug.append(role)
        db.session.add(cust)
        db.session.commit()
        return user

    def create_device_model(self):
        device_model = sdDeviceModel(
            id=0,
            name="test_device_model",
            display_name="Test Device Model",
            comment="For Unit Test")

        db.session.add(device_model)
        db.session.commit()

    def login(self, cust=None, user=None):
        import json
        if not cust:
            cust = self.cust_name
        if not user:
            user = self.user_name
        resp = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({"custname": cust,
                             "username": user,
                             "password": self.user_pass}),
            content_type="application/json"
        )
        data = json.loads(resp.data.decode())
        token = data['token'].get('access_token')
        self.token = token
        return token

    def create_app(self):
        app.config.from_object("app.main.config.TestingConfig")
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()
        self.user = self.create_cust_user_user_group()
        self.create_device_model()
        self.create_privilege()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
