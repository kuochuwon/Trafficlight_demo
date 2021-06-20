import requests
import time

url = "http://127.0.0.1:5000/api/v1/device/1/getall"


payload = {"user": "roy",
           "max_device": 0}
tStart1 = time.time()
response = requests.post(url, json=payload)
tEnd1 = time.time()
# print(response.text)
print(f"execute post function total costs: {round(tEnd1-tStart1,2)} secs")
