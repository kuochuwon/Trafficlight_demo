import json

from app.test.base import BaseTestCase
from app.test.stubs.data import compose_input_for_device, compose_input_for_schedule, FakeDataCreation
from app.test.stubs.pseudo_device_creating import (add_user_groups,
                                                   user_insertion,
                                                   check_device_input,
                                                   check_device_refans,
                                                   check_device_group_input,
                                                   check_device_group_refans,
                                                   check_user_input,
                                                   check_user_refans,
                                                   check_user_group_input,
                                                   check_user_group_refans,
                                                   check_schedule_input,
                                                   check_schedule_refans)


class TestCheckIfExist(BaseTestCase):
    def test_device(self):
        # TAG db initialize
        FakeDataCreation().insert_device_model(2)
        input_data = compose_input_for_device(3)
        token = self.login()
        self.client.post("/api/v1/device/add",
                         data=json.dumps(input_data),
                         content_type="application/json",
                         headers={"Authorization": f"Bearer {token}"})

        input_data = check_device_input()
        resp = self.client.post("api/v1/check/check_db",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})
        output = json.loads(resp.data.decode())
        output = json.dumps(output, indent=4)
        refans = check_device_refans()
        refans = json.dumps(refans, indent=4)

        self.assertEqual(output, refans)

    def test_device_group(self):
        FakeDataCreation().insert_device_model(2)
        token = self.login()
        sample_data = [("麥當勞", "雞塊旁的路燈"), ("肯德基", "雞米花上的路燈"), ("漢堡王", "小華堡裡的路燈")]
        input_data = {"device_groups": [dict(name=name[0],
                                             display_name=name[1]) for count, name in zip(range(3), sample_data)]}
        resp = self.client.post("/api/v1/device/group/add",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})
        input_data = check_device_group_input()
        resp = self.client.post("api/v1/check/check_db",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})
        output = json.loads(resp.data.decode())
        output = json.dumps(output, indent=4)
        refans = check_device_group_refans()
        refans = json.dumps(refans, indent=4)
        self.assertEqual(output, refans)

    def test_user(self):
        user_insertion()
        input_data = check_user_input()
        token = self.login()
        resp = self.client.post("api/v1/check/check_db",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})
        output = json.loads(resp.data.decode())
        refans = check_user_refans()
        self.assertEqual(output, refans)

    def test_user_group(self):
        input_data = add_user_groups()
        token = self.login()
        resp = self.client.post("api/v1/account/group/add",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})
        input_data = check_user_group_input()
        resp = self.client.post("api/v1/check/check_db",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})
        output = json.loads(resp.data.decode())
        refans = check_user_group_refans()
        self.assertEqual(output, refans)

    def test_schedule_group(self):
        input_data = compose_input_for_schedule(3)
        token = self.login()
        resp = self.client.post("api/v1/schedule/add",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})
        input_data = check_schedule_input()
        resp = self.client.post("api/v1/check/check_db",
                                data=json.dumps(input_data),
                                content_type="application/json",
                                headers={"Authorization": f"Bearer {token}"})
        output = json.loads(resp.data.decode())
        refans = check_schedule_refans()
        self.assertEqual(output, refans)
