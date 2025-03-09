from vk_api import VkUpload, VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def captcha_handler(captcha):
   print('Введите код капчи: ' + captcha.get_url())
   key = input('>>')
   captcha.try_again(key)

login = 'timoncraus@list.ru'
password = '007007007оо'
vk_session = VkApi(login=login, password=password, app_id=2685278, captcha_handler=captcha_handler)
vk_session.auth(token_only=True, token=)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

api = vk.API(session)

print('Бот готов')
for event in longpoll.listen():
   if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.from_user:
      if event.text == '1':
         vk.messages.send(peer_id=event.user_id, message='2', random_id=get_random_id())