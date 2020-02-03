import requests
import json
import random
import datetime
from user import UserList

class Server:
    group_id = 191177272
    access_token = 'access_token=f068c796542cba0f4dbdd0f6e39ba656a489731d36cfdcbdf7cee30de822ae000aa9e1aa8293bc61d77c7'
    v = 'v=5.103'  # Текущая версия VkAPI
    body = 'https://api.vk.com/method/'  # Тело запроса
    data = UserList()
    closest_time = 'z' # to make it bigger than numbers
    closest_events = dict()

    def __init__(self):
        Server.getLongPollServer(self)

    def find_closest_events(self):
        for key, value in self.data.get_dict().items():
            for sub_key, sub_value in value.items():
                if sub_key <= self.closest_time:
                    self.closest_time = sub_key
                    self.closest_events[key] = sub_value

    def getLongPollServer(self):
        method = 'groups.getLongPollServer?group_id=191177272'
        reply = requests.get("&".join([Server.body + method, Server.v, Server.access_token]))
        data = json.loads(reply.text)
        self.server = data['response']['server']
        self.key = data['response']['key']
        self.ts = data['response']['ts']
        # print(self.server, self.key, self.ts)

    def simple_request(self):
        method = self.server + '?act=a_check&key=' + self.key + '&ts=' + self.ts + "&wait=25"
        return requests.get(method)

    def simple_loop(self):
        reply = json.loads(self.simple_request().text)
        self.ts = reply['ts']
        # print(json.dumps(reply, indent='\t'))
        if reply['updates']:
            message = reply['updates'][0]['object']['message']['text']
            user_id = reply['updates'][0]['object']['message']['from_id']
            self.data.add_rec(str(user_id), {datetime.datetime.now().strftime('%Y-%m-%d:%H.%M'): message})
            random_id = random.randint(0, 100)
            method = 'messages.send?' + 'user_id=' + str(user_id) + '&random_id=' + str(random_id) \
                     + '&message=' + message
            r = requests.get("&".join([Server.body + method, Server.v, Server.access_token]))
            print("&".join([Server.body + method, Server.v, Server.access_token]))
        self.simple_loop()

    def check_date(self, time):
        if datetime.datetime.now().strftime('%Y-%m-%d:%H.%M') == time:
            return 1
        return 0


server = Server()
server.simple_loop()
