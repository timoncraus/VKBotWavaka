# coding=utf-8
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

import time

id_list = [660375107]
group_id = 192082307
my_token = 'a275ef4cebed4bcb40c997fe869363e0b595d6e26170359606313ce8cdd53b56ebac4a52e175215f17895'

vk_session = VkApi(token=my_token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

while True:
	print('Бот готов')
	try:
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.from_user:

				rezult = vk_session.method('messages.getById', {'message_ids':[event.message_id], 'group_id':192082307})
				try:
					attachment_list = []
					for i in rezult['items'][0]['attachments']:
						photo = i['photo']
						attachment = 'photo{}_{}_{}'.format(photo['owner_id'], photo['id'], photo['access_key'])
						attachment_list.append(attachment)
					#photo = rezult['items'][0]['attachments'][0]['photo']
					
				except:
					attachment = None
				for id in id_list:
					if id != event.user_id:
						vk.messages.send(message = '@id' + str(event.user_id) + '\n' + event.text, random_id = get_random_id(), 
							user_id = id, attachment=attachment_list)

				vk.messages.send(message = 'Успешно отправлено администраторам', random_id = get_random_id(), user_id = event.user_id)
	except Exception as E:
		print('Ошибка: ' + str(E))
		print('Перезапуск...')
		time.sleep(1)
	