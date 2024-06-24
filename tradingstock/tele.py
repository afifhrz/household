import requests
import os

class Tele():
    def __init__(self):
        tele_token = os.environ['TELE_TOKEN']
        self.baseurl = f"https://api.telegram.org/bot{tele_token}/sendMessage"
        self.body = {}

    async def sendMessage(self, text):
        try:
            self.body["chat_id"] = "-4243707771"
            self.body['text'] = "<pre>\n"+text+"\n</pre>"
            self.body['parse_mode'] = "html"
            response = requests.post(self.baseurl, json = self.body)
            # print(response.text)
        except Exception as e:
            raise e