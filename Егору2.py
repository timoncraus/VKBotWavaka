# coding=utf-8
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

import time
from rcon import rcon

my_token = 'a275ef4cebed4bcb40c997fe869363e0b595d6e26170359606313ce8cdd53b56ebac4a52e175215f17895'
host1 = ''
password = ''

vk_session = VkApi(token=my_token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

while True:
	print('Бот готов')
	try:
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.from_user:

				response = await rcon(event.text, host=host1, port=5000, passwd=password)
				
				vk.messages.send(message = response, random_id = get_random_id(), user_id = event.user_id)
	except Exception as E:
		print('Ошибка: ' + str(E))
		print('Перезапуск...')
		time.sleep(1)
	