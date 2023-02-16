import json

import requests


def send_text(num, text):
    url = "https://konnect.dotgo.com/api/v1/Accounts/pYflVu4c7hIexfzoH5fP8Q==/Messages"

    #payload = "{\r\"id\":\"\",\r\"to\":[\"+2348077369823\"],\r\"sender_mask\":\"TECHTRIAL\",\r\"body\":\"Your charging for Subscription is successful, you are subscribed for a period of 30 days\"\r}\r"
    #payload = "{\r\"id\":\"98939390hdhdhn\",\r\"to\":[test,\"91888100XXXX\"],\r\"sender_mask\":\"TECHTRIAL\",\r\"body\":\"Your charging for Subscription is successful, you are subscribed for a period of 30 days\"\r}\r"
    payload={
        "id":"98939390hdhdhn",
        "to":[num],
        "sender_mask":"Mperial",
        "body":text,


    }
    headers = {
        'Content-Type': "application/json",
        'Authorization': "3NuTIO5vw+L6qg7dvTUKyR9cnl+MqK25mFsBqtvWacA="
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

