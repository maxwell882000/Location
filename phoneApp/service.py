import json

from django.utils.baseconv import base64
import requests

from logApp.models import AppLog



class PhoneException(Exception):
    pass


class PhoneService:
    login = "MSK_iplmshp"
    password = "uFAZ35VK"
    URL = "https://a2p-api.megalabs.ru/sms/v1/sms"
    FROM = "IPLemeshkin"

    # def __init__(self):
    #     self.base_64 = base64("{}:{}".format(self.login, self.password))

    def sendCode(self, phone: int, message: str) -> bool:
        response = requests.request("POST",
                                    auth=(self.login, self.password),
                                    data=json.dumps({
                                        'from': self.FROM,
                                        'to': phone,
                                        'message': message,
                                    }), url=self.URL)
        print(response.content)
        if response.status_code == 200:
            content = response.json()
            if content['result']['status']['code'] == 0:
                return True
            raise PhoneException(content['result']['status']['description'])
        
        return False


