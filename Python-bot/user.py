# coding=utf-8
import json
import datetime

class UserList:
    all_users = dict()  # Contains dict(user_id, User)
    data_dir = ''

    def __init__(self, data_dir="./data/base.json"):
        self.data_dir = data_dir
        f = open(data_dir, 'r', encoding="utf-8")
        for key, value in json.loads(f.read()).items():
            for sub_key, sub_value in value.items():
                if sub_key >= datetime.datetime.now().strftime('%Y-%m-%d:%H.%M'):
                    self.all_users[key] = {sub_key: sub_value}
        print(self.all_users)
        f.close()

    def add_rec(self, user_id, user_events=None):
        if user_events is None:
            user_events = {}
        if self.all_users.get(user_id) is None:
            self.all_users[user_id] = user_events
        else:
            self.all_users[user_id] = {**self.all_users[user_id], **user_events}
        self.update_file()

    def update_file(self):
        f = open(self.data_dir, 'w', encoding="utf-8")
        f.write(json.dumps(self.all_users))
        f.close()

    def get_dict(self):
        return self.all_users

    def delete_event(self, user_id, date):
        self.all_users[user_id].pop(date)
