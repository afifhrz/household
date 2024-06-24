import requests

class Tele():
    def __init__(self):
        self.baseurl = "https://api.telegram.org/bot7453140768:AAFIKzbCcnVOagPa6Ja3anQlTaAdoNR-eu4/sendMessage"
        self.body = {}

    async def sendMessage(self, text):
        try:
            self.body["chat_id"] = "-4243707771"
            self.body['text'] = "<pre>\n"+text+"\n</pre>"
            self.body['parse_mode'] = "html"
            response = requests.post(self.baseurl, json = self.body)
            print(response.text)
        except Exception as e:
            raise e