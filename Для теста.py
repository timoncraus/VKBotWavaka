# coding=utf-8
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

import time

import pyowm #погода

vk_session = VkApi(token='2c73aa7be44fde264bff2ddca9c21edbf9486beb8f3b560534bb1ff99c72317acfe794824280bfa968c01')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

idslov = {}

while True:
	print('Бот готов')
	try:
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.from_user:
				vksms = event.text.lower()
				if not (event.user_id in idslov):
					idslov[event.user_id] = 'menu'
				if idslov[event.user_id] == 'menu':
					keyboard = VkKeyboard(one_time=True)
					keyboard.add_button('Привет', color=VkKeyboardColor.PRIMARY)
					if vksms.count('прив') > 0 or vksms.count('здаров') > 0 and not(vksms.count('привив') > 0) and not(vksms.count('привит') > 0):
						vk.messages.send(user_id=event.user_id, message='Привет', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('хай') > 0 or vksms.count('хелло') > 0 or vksms.count('хело') > 0:
						vk.messages.send(user_id=event.user_id, message='Хаю хай)', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('скажи') > 0 and vksms.count('мой') > 0 and (vksms.count('айди') > 0 or vksms.count('id') > 0):
						vk.messages.send(user_id=event.user_id, message='Вот твой id:', random_id=get_random_id(), keyboard=keyboard.get_keyboard()) #здесь клавиатуру можно отправлять, а можно не отправлять
						vk.messages.send(user_id=event.user_id, message= event.user_id, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms == 'переслать':
							vk.messages.send(user_id=event.user_id, message='пересылаю', random_id=get_random_id(),
								keyboard=keyboard.get_keyboard(), reply_to= event.message_id)
					# Вызов погоды
					elif vksms.count('погод') > 0:
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='В каком городе/стране вы бы хотели узнать погоду?', random_id=get_random_id(),
							keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'weath'

					else:
						if event.text != '':
							vk.messages.send(user_id=event.user_id, message='Извини, я не знаю, что ответить на "' + event.text + '"',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						else:
							vk.messages.send(user_id=event.user_id, message='Извини, я не знаю, что ответить на это',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard(), reply_to= event.message_id)
				elif idslov[event.user_id] == 'weath':
					keyboard = VkKeyboard(one_time=True)
					keyboard.add_button('Привет', color=VkKeyboardColor.PRIMARY)
					if vksms == 'отмена':
						vk.messages.send(user_id=event.user_id, message='Погода закрыта', random_id=get_random_id(),
							keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						try:
							owm = pyowm.OWM('2b81034cf1e96c904e721b0da1ad3f9d', language="ru")
							observ = owm.weather_at_place(event.text)
							w = observ.get_weather()
							temp = w.get_temperature('celsius')["temp"]
							hum = w.get_humidity()
							time = w.get_reference_time(timeformat='iso')
							wind = w.get_wind()["speed"]
							status = w.get_detailed_status()
							Weather = 'В ' + event.text[0].upper() + event.text[1:].lower() + ' сейчас ' + w.get_detailed_status() + '\nТемпература сейчас в районе ' + str(temp) + 'C\nСкорость ветра: ' + str(wind) + ' м/с' + '\nВлажность: ' + str(hum) + '%\nДата/Время: ' + str(time)
							idslov[event.user_id] = 'menu'
						except:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							Weather = 'Извините, я не знаю такого города или страны, попробуйте ещё раз'
						vk.messages.send(user_id=event.user_id, message=Weather, random_id=get_random_id(),
							keyboard=keyboard.get_keyboard())


	except Exception as E:
		print('Ошибка: ' + str(E))
		print('Перезапуск...')
		time.sleep(1)