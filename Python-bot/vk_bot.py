import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests

vk_session = vk_api.VkApi(token="f068c796542cba0f4dbdd0f6e39ba656a489731d36cfdcbdf7cee30de822ae000aa9e1aa8293bc61d77c7")

vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 191177272)

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_user:
            msg = 'Не понимаю тебя' if event.obj.get('message').get('attachments') != [] else event.obj.get('message').get('text')
            vk.messages.send(
                user_id=event.obj.get('message').get('from_id'),
                random_id=get_random_id(),
                message=msg,
            )
