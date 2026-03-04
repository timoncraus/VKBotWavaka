# coding=utf-8
import time
import requests
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
# + Доп модули:
import traceback # подробный вывод ошибок
import random #рандом

import datetime #время

import wikipedia #википедия
wikipedia.set_lang("RU")

import pyowm #погода
from pyowm.utils.config import get_default_config
config_dict = get_default_config()
config_dict['language'] = 'ru' 

from pycbrf.toolbox import ExchangeRates #валюта

import matplotlib #график
import matplotlib.pyplot as plt
from urllib.parse import urlencode
from urllib.request import urlopen

import os # для автомат. удаления фалов
from deep_translator import GoogleTranslator # переводчик

PATH1 = os.path.dirname(os.path.abspath(__file__))

# Получение данных о id пользователей
#print('Запускаем бота на:')
#print('1 - На компьютере')
#print('2 - На сервере (по умолчанию)')
#print('3 - Указать путь к файлам самостоятельно')
#fhg = str(input('>>>'))
#if fhg == '1':
fhg = '1'
file = 'idlist.txt'
file2 = 'stab.txt'
uuu = 0
uum = 0
#elif fhg == '3':
#	file = str(input('Введите путь к файлу с id пользователей:'))
#	file2 = str(input('Введите путь к файлу с количеством сообщением:'))
#	uuu = 0
#	uum = 0
#else:
#	file = '/home/ttimoncraus/idlist - vk_bot.txt'
#	file2 = '/home/ttimoncraus/stab.txt'
#	uuu = 0
#	uum = 0

f = open(file, 'r')
idlist = map(int, (f.read()).split())
f.close()
idslov = {}
for id in idlist:
	idslov[id] = 'menu'
morslov = {}
for id in idlist:
	morslov[id] = '0'

f = open(file2, 'r')
stab = int(f.read())
f.close()
# Настройка vk
token1 = 'vk1.a.5h8UlPZpAWwaE3oX09oFnH0QeNXl60JYRjuPqiHGT3fbMQDbNWjwNbP4b-Cs8geTkgpCetgEKw3Cv0hwwvd5Veo0Q6w7gl5Zcg6hTACVKr1oa6jBPILGdzy53odxfQTVmxVuKEwmHxHQpWIuOBHY-Z3nW4MUalU7z1A1NSRCuvhM4lhyCmq1ESi2jX951JCm1ypCId7ZBDjDajtFirgVkQ'
group_id = '236424469'
vk_session = vk_api.VkApi(token=token1)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
# Некоторые переменные:
sub = ''
version = '2.3'
str_skills = 'Я бот-эрудит. Авторы: Горшков Тимофей, Мендыгалиев Данияр, Барсуков Максим (2026 г.). Вот, что я умею:' \
			 '\n⭐ Напиши "википедия", "вики", "wikipedia", "wiki" и т.д., чтобы найти что-либо в Википедии' \
			 '\n⭐ Напиши "переводчик", "перевод", "переведи", "перевести" и т.д., чтобы перевести текст с одного языка на другой' \
			 '\n⭐ Напиши "скажи погоду", "узнать погоду", "погода" и т.д., чтобы узнать погоду в том или ином городе/стране' \
			 '\n⭐ Напиши "время", "день недели", "сезон" и т.д., чтобы узнать в каком временном отрезке ты сейчас находишься'\
			 '\n⭐ Напиши "сколько дней в сентябре", "сколько дней в марте" и т.д., чтобы узнать количество дней в том или ином месяце' \
			 '\n⭐ Напиши "стабильность", чтобы узнать, сколько бот отправил сообщений, начиная с 04.03.26' \
             '\n🔆 А вообще можешь просто со мной поболтать😄'
str_data_v = 'Версия ' + version + '\nДаты других версий: ' \
								   '\n"test_group", "bot_tima" - 1.0 (17.02.2020)' \
								   '\n"Wavaka" - 2.0 (23.02.20)' \
								   '\n"Wavaka" - 2.1 (8.03.20)' \
								   '\n"Wavaka" - 2.2 (27.03.20)' \
								   '\n"Wavaka" - 2.3 (22.04.20)'

# Функции:
def get_main_menu_keyboard():
	keyboard = VkKeyboard(one_time=True)
	keyboard.add_button('Википедия', color=VkKeyboardColor.PRIMARY)
	keyboard.add_button('О программе', color=VkKeyboardColor.POSITIVE)
	keyboard.add_line()
	keyboard.add_button('Сколько дней в сентябре', color=VkKeyboardColor.SECONDARY)
	keyboard.add_line()
	keyboard.add_button('Переводчик', color=VkKeyboardColor.SECONDARY)
	keyboard.add_button('Время', color=VkKeyboardColor.SECONDARY)
	keyboard.add_line()
	keyboard.add_button('Погода', color=VkKeyboardColor.SECONDARY)
	keyboard.add_button('Факты', color=VkKeyboardColor.SECONDARY)
	return keyboard

def subscribe(user_id, group_id, token):  # Узнать, подписан или нет (возвращает True или False)
	if vk.groups.isMember(access_token=token, group_id=group_id, user_id=user_id):
		# Проверяем является ли пользователь участником сообщества
		return True
	return False
def add_photo(url):    # Добавить фото: туда строчку с url фотки; возвращает фотку, которую надо вложить в attachment, когда отправляешь сообщение
	attachments = []
	upload = VkUpload(vk_session)
	image = requests.get(url, stream=True)
	photo = upload.photo_messages(photos=image.raw)[0]
	attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
	return ','.join(attachments)
def add_many_photo(list):  # Добавить много фото: туда запихнуть список с url фоток; возвращает список, который надо вложить в attachment, когда отправляешь сообщение
	attachments = []
	upload = VkUpload(vk_session)
	for url in list:
		image = requests.get(url, stream=True)
		photo = upload.photo_messages(photos=image.raw)[0]
		attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
	return ','.join(attachments)
def add_photo_from_computer(url):  # Добавить фото: туда строчку с расположением фотки на компе; возвращает фотку, которую надо вложить в attachment, когда отправляешь сообщение
	upload = vk_api.VkUpload(vk)
	photo = upload.photo_messages(url)
	owner_id = photo[0]['owner_id']
	photo_id = photo[0]['id']
	access_key = photo[0]['access_key']
	phh = f'photo{owner_id}_{photo_id}_{access_key}'
	return phh

def fact(): # Список фактов (возвращает факт в строке)
	facts = ['1525000000 км телефонного провода натянуто по всей территории США.', '111111111х111111111 = 123456789е+16',
		'160 автомобилей могут ехать бок о бок на Монументальном Вале что находится в городе Бразилиа и является самой широкой дорогой в мире.',
		'166875000000. Столько посылок доставляется каждый год в США.',
		'5% канадцев не знаю, первые 7 слова канадского гимна, но знаю первые 9 американского гимна, а 7% американцев не знают, первые 9 слова американского гимна, но знаю первые 7 канадского гимна.',
		'85000000 тонн бумаги используются каждый год в США.', 'Кошка имеет 32 мышцы в каждом ухе.',
		'Таракан может прожить несколько недель с отрубленной головой.',
		'Компания в Тайване делают посуду из пшеницы, так что вы можете съесть тарелку.',
		'Корова производит в 200 раз больше газа в день, чем человек.', '1 Цент имеет 118 хребтов по краям монеты',
		'Полностью загруженому супертанкеру необходимо не менее двадцати минут, чтобы остановить.',
		'Жираф может чистить уши своим 21-дюймовым языком.', 'Жираф может обходиться без воды дольше, чем верблюд.',
		'Золотая рыбка имеет память течение трех секунд.', 'Сердце ежа в среднем бьется 300 раз в минуту.',
		'Колибри весит меньше копейки.', 'Медуза на 95 процентов состоит из воды.', '"Миг" длится 1/100-й секунды.',
		'Аэробус использует 4000 галлонов топлива на взлет.', 'Человек по имени Чарльз Осборн икает в течение 6 лет.',
		'Крот может выкопать тоннель 300 футов в длину всего за одну ночь.', 'Оргазм свиньи длится 30 минут.',
		'Акула единственная рыба, которая может моргать обоими глазами.',
		'Акула может почуствовать каплю крови в 100 миллионах литров воды.',
		'Скунс может распылять свои вонючие аромат более чем 10 футов (~3 метра).',
		'При чихании поток воздуха из вашего рта выходит со скоростью более 100 миль/ч (~160 км/ч)',
		'Зубочистка является объектом которым чаще всего давятся американцы.',
		'По данным британского закона, принятого в 1845 году, тем, кто пытался покончить жизнь самоубийством, был приговорен к смертной казне.',
		'Все часы в фильме "Криминальное чтиво" застряли на 4:20.', 'Древние египтяне спали на подушках из камня.',
		'В среднем человек смеется 15 раз в день.', 'Игуана может находиться под водой в течение 28 минут.',
		'Глаз у страуса больше, чем его мозг.',
		'Дети рождаются без коленных чашечек. Они не появляются до достижения ребенком 2-6 лет.',
		'Жевательная резинка содержит каучук.', 'Верблюды имеют три веки, чтобы защитить себя от песчаных бурь.',
		'Моча кошек светится под ультрафиолетом.',
		'Кошки могут производить более ста вокальных звуков, а собаки могут производить только около десяти.',
		'Дельфины спят с одним открытым глазом.',
		'Комиксы "Дональд Дак" были запрещены в Финляндии, потому что он не носит брюки.',
		'Каждый раз, когда Бетховен садился писать музыку, он наливал ледяной воды себе на голову.',
		'Февраль 1865 является единственным месяцем в истории человечества не имеющим полной луны.',
		'Ногти на руках растут почти в 4 раза быстрее, чем ногти на ногах.', 'Жирафы не имеют голосовых связок.',
		'"Я." является кратчайшим предложением в русском языке.',
		'В 1980 году была только одна страна в мире, где нет телефонов - Бутан.',
		'В большинстве рекламных объявлений, в том числе газеты, время, показанное на часах, равняется 10:10.',
		'В космосе астронавты не могут плакать, потому что нет никакой тяжести и слезы не могут течь.',
		'Леонардо да Винчи изобрел ножницы.', 'Деньги сделаны не из бумаги, а из хлопка.',
		'Большинство коров дают больше молока при прослушивании музыки.',
		'Четверть костей в вашем теле находятся в ногах.', 'Только 55% американцев знают, что Солнце является звездой.',
		'По статистике только один человек из двух миллиардов может жить до 116 лет и старше.',
		'Наши глаза всегда одного размера с рождения, однако наш нос и уши никогда не перестают расти.',
		'В среднем человек засыпает за семь минут.', 'В среднем человек имеет более чем 1460 мечтаний в год.',
		'В среднем человек находится примерно на четверть дюйма (32 мм) выше в ночное время.',
		"Земля весит около 6'588'000'000'000'000'000'000'000 тонн.",
		'Электрический стул был изобретен стоматологом Альфредом Саутвиком. Если интересно, почитай:\nhttps://yandex.ru/turbo?text=https%3A%2F%2Fribalych.ru%2F2015%2F08%2F07%2Felektricheskij-stul%2F',
		'Слон единственное млекопитающее, которое не умеет прыгать.',
		'Самая высокая точка в Пенсильвании ниже, чем самая низкая точка в штате Колорадо.',
		'Мозг неандертальца был больше, чем сейчас наш.',
		'Самая первая бомба, сброшенная на Берлин во время Второй Мировой Войны убила только слона в Берлинском зоопарке.',
		'Слово "Шах и мат" в шахматах происходит от персидского фраза "Шах-Мат», что означает «король мертв».',
		'Тигры еще имеют полосатую кожу, а не только полосатый мех.',
		'Женские сердца в среднем бьются быстрее, чем у мужчин.', 'Ты моргаешь более 20 миллионов раз в год.',
		'Ты рождаешься с 300 костями, но когда ты становишься взрослым, у тебя остается только 206.',
		"Ваше сердце бьется более 100'000 раз в день.", 'Правое легкое забирает больше воздуха, чем левое.',
		'Ваш желудок должен производить новый слой слизи каждые две недели, иначе он будет переваривать сам себя.']
	act_fact = random.choice(facts)
	return act_fact

def weekday(): # Узнать день недели (возвращает строку типа "среда")
	a = datetime.datetime.today().isoweekday()
	if a == 1:
		return 'Понедельник'
	elif a == 2:
		return 'Вторник'
	elif a == 3:
		return 'Среда'
	elif a == 4:
		return 'Четверг'
	elif a == 5:
		return 'Пятница'
	elif a == 6:
		return 'Суббота'
	elif a == 7:
		return 'Воскресенье'
def month(): # Узнать месяц (возвращает строку типа "Августа")
	now = datetime.datetime.now()
	m = now.month
	if m == 1:
		return 'Января'
	elif m == 2:
		return 'Февраля'
	elif m == 3:
		return 'Марта'
	elif m == 4:
		return 'Апреля'
	elif m == 5:
		return 'Мая'
	elif m == 6:
		return 'Июня'
	elif m == 7:
		return 'Июля'
	elif m == 8:
		return 'Августа'
	elif m == 9:
		return 'Сентября'
	elif m == 10:
		return 'Октября'
	elif m == 11:
		return 'Ноября'
	elif m == 12:
		return 'Декабря'
def month2(): # Узнать месяц 2.0 (возвращает строку типа "Август")
	now = datetime.datetime.now()
	m = now.month
	if m == 1:
		return 'Январь'
	elif m == 2:
		return 'Февраль'
	elif m == 3:
		return 'Март'
	elif m == 4:
		return 'Апрель'
	elif m == 5:
		return 'Май'
	elif m == 6:
		return 'Июнь'
	elif m == 7:
		return 'Июль'
	elif m == 8:
		return 'Август'
	elif m == 9:
		return 'Сентябрь'
	elif m == 10:
		return 'Октябрь'
	elif m == 11:
		return 'Ноябрь'
	elif m == 12:
		return 'Декабря'
def month3(): # Узнать месяц 3.0 (возвращает строку типа "Августе")
	now = datetime.datetime.now()
	m = now.month
	if m == 1:
		return 'Январе'
	elif m == 2:
		return 'Феврале'
	elif m == 3:
		return 'Марте'
	elif m == 4:
		return 'Апреле'
	elif m == 5:
		return 'Мае'
	elif m == 6:
		return 'Июне'
	elif m == 7:
		return 'Июле'
	elif m == 8:
		return 'Августе'
	elif m == 9:
		return 'Сентябре'
	elif m == 10:
		return 'Октябре'
	elif m == 11:
		return 'Ноябре'
	elif m == 12:
		return 'Декабре'
def season(): # Узнать сезон (возвращает строку типа "лето")
	now = datetime.datetime.now()
	m = now.month
	if m == 12 or m == 1 or m == 2:
		return 'зима'
	elif m == 3 or m == 4 or m == 5:
		return 'весна'
	elif m == 6 or m == 7 or m == 8:
		return 'лето'
	elif m == 9 or m == 10 or m == 11:
		return 'осень'

def repetition(row: str): #есть ли повторение в строке - True, если уникальны
	return True if sorted(list(row)) == sorted(list(set(row))) else False

def out_game(t):
	if t == 'отмена' or t == 'выйти' or t == 'закончить' or t == 'прекратить'  or t == 'хватит' or t == 'достаточно' or t == 'назад' or t == 'вернуться':
		return True
	else:
		return False

# Сам бот:
while True:
	print('Бот готов')
	try:
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
				stab+=1
				f = open(file2, 'w')
				f.flush()
				f.write(str(stab))
				f.close()
				vksms = event.text.lower()
				# Если впервые написал боту:
				if not (event.user_id in idslov):
					f = open(file, 'a')
					f.write(' ' + str(event.user_id))
					f.close()
					idslov[event.user_id] = 'menu'
				# Если не подписан, напоминаем:
				if not (subscribe(event.user_id, group_id, token1)):
					sub = '\nКстати, ты забыл подписаться🐔'
				else:
					sub = ''
				# Сами ответы на сообщения:
				if idslov[event.user_id] == 'menu':
					keyboard = get_main_menu_keyboard()
					# Разговорный
					if vksms == 'начать':
						vk.messages.send(user_id=event.user_id, message='Ну начинай))' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('вперед') > 0 or vksms.count('вперёд') > 0:
						vk.messages.send(user_id=event.user_id, message='Только вперёд!' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif event.text == 'P.S.':
						vk.messages.send(user_id=event.user_id, message='P.S. Не стесняйся писать боту нестандартным путем, не по шаблону. Я многому его научил и он на многое откликается. '
						'Например, ему абсолютно без разницы, будешь ли ты ему писать с большой или с маленькой буквы; '
						'чтобы вернуться обратно, напишешь ли ты "Отмена" или "Хватит", "Достаточно" и т.д. '
						'В конце концов это разговорный бот)\n Если бот чего-то не понял или ты заметил какой-то баг, обязательно пиши мне! '
						'Будем прогрессировать бота все вместе!\n(если ты не знаешь кто я, попроси его сказать админа)',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms == 'что за палки /?':
						vk.messages.send(user_id=event.user_id, message='Ты конечно можешь заменить "/" на пробел, однако ВК автоматически заменяет двойной пробел на обычный и с этим ничего не поделаешь, уж извини. Приходится как-то выкручиваться' + sub,random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('прив') > 0 or vksms.count('здаров') > 0 and not(vksms.count('привив') > 0) and not(vksms.count('привит') > 0):
						vk.messages.send(user_id=event.user_id, message='Приветик' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('хай') > 0 or vksms.count('хелло') > 0 or vksms.count('хело') > 0:
						vk.messages.send(user_id=event.user_id, message='Хаю хай)' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('здравствуй') > 0 or vksms == 'доброго времени суток':
						vk.messages.send(user_id=event.user_id, message='Здрасьте' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif (vksms.count('добр') > 0 and vksms.count('утр') > 0) or vksms.count('утречко') > 0:
						vk.messages.send(user_id=event.user_id, message='Доброе' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('добр') > 0 and (vksms.count('день') > 0 or vksms.count('вечер')):
						vk.messages.send(user_id=event.user_id, message='Добрый' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif ((vksms.count('спокойной') > 0 or vksms.count('добр') > 0) and vksms.count('ночи') > 0) or (vksms.count('сладких') > 0 and vksms.count('снов') > 0):
						vk.messages.send(user_id=event.user_id, message='Спокойной ночи🌠' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('пока') > 0 or (vksms.count('до') > 0 and vksms.count('встречи') > 0) or (
						vksms.count('до') > 0 and (vksms.count('связи') > 0 ) or vksms.count('завтра') > 0) or vksms.count(' бай') > 0 or vksms.count('бай ') > 0 or vksms == 'бай':
						vk.messages.send(user_id=event.user_id, message='Пока-пока👋🏻' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif (vksms.count('до') > 0 and vksms.count('свидания') > 0) or vksms.count('досвидос') > 0:
						vk.messages.send(user_id=event.user_id, message='До свидания👋🏻' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('спасибо') > 0:
						vk.messages.send(user_id=event.user_id, message='Пожалуйста😊' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('увидимся') > 0:
						vk.messages.send(user_id=event.user_id, message='Конечно увидимся👋🏻' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('спишемся') > 0:
						vk.messages.send(user_id=event.user_id, message='Конечно спишемся👋🏻' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('услышимся') > 0:
						vk.messages.send(user_id=event.user_id, message='Ну, слабо верится, но, думаю, когда-нибудь это произойдет😅' + sub,
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('это') > 0 and vksms.count('красти') > 0 and vksms.count('крабс') > 0:
						vk.messages.send(user_id=event.user_id, message='Нет, это Патрик🙃' + sub,
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif (vksms.count('как') > 0 and vksms.count('дел') > 0) or (vksms.count('как') > 0 and vksms.count('настроение') > 0):
						vk.messages.send(user_id=event.user_id, message='Просто замечательно!😊' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif (vksms.count('что') > 0 or vksms.count('че') > 0) and (vksms.count('нового') > 0 or vksms.count('обновили') > 0):
						vk.messages.send(user_id=event.user_id, message='Вот, что нового в последней версии:'
						 '\n🎦 Обновление функции "Что посмотреть" в честь карантина - добавлено аниме'
						 '\n🌟Подробности всего этого вы можете найти, написав боту "что ты умеешь", "умения", "способности" и т.д.'
						 + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif ((vksms.count('что') > 0 or vksms.count('че') > 0) and vksms.count('делаешь') > 0) or vksms == ('чд') or (vksms.count('чем') > 0 and (vksms.count('занят') > 0 or vksms.count('занимаешься') > 0)):
						vk.messages.send(user_id=event.user_id, message='С тобой сижу разговариваю😊' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('как') > 0 and event.text.count('здоровье') > 0:
						vk.messages.send(user_id=event.user_id, message='Отлично' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif ((vksms.count('че') > 0 or vksms.count('чё') > 0) and not(vksms.count('чет') > 0 or vksms.count('чёт') > 0)) and vksms.count('как') > 0:
						vk.messages.send(user_id=event.user_id, message='Нормаально😎' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif ((vksms.count('че') > 0 or vksms.count('чё') > 0) and not(vksms.count('чет') > 0 or vksms.count('чёт') > 0)) and vksms.count('кого') > 0:
						vk.messages.send(user_id=event.user_id, message='Все просто отлично😎' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif ((vksms.count('какой') > 0 or vksms.count('какая') > 0) and vksms.count('любим') > 0) or (
						(vksms.count('какой') > 0 or vksms.count('какая') > 0 or vksms.count('что') > 0) and vksms.count('лучше') > 0) or (vksms.count('или') > 0 and vksms.count('?') > 0):
						vk.messages.send(user_id=event.user_id, message='Эм... Ну не знаю, мне все нравится😶' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('какие') > 0 and vksms.count('планы') > 0:
						vk.messages.send(user_id=event.user_id, message='Пока никаких, но все зависит от тебя😉' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif ((vksms.count('как') > 0) and vksms.count('поживаешь') > 0) or (vksms.count('как') > 0 and vksms.count('ты') > 0):
						vk.messages.send(user_id=event.user_id, message='Хорошо🙂' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif (vksms.count('чем') > 0 and vksms.count('нравится') > 0 and vksms.count('заниматься') > 0) or (vksms.count('что') > 0 and vksms.count('любишь') > 0 and vksms.count('делать') > 0):
						vk.messages.send(user_id=event.user_id, message='Отвечать всем на сообщения и приносить добро🤗' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('нравится') > 0 or vksms.count('любишь') > 0:
						vk.messages.send(user_id=event.user_id, message='Конечно, более чем!' + sub, random_id=get_random_id())
					elif vksms.count('кто') > 0 and vksms.count('я') > 0:
						vk.messages.send(user_id=event.user_id, message='Ты очень хороший человек🤗' + sub, random_id=get_random_id())
					elif vksms.count('я') > 0 and vksms.count('подписал') > 0:
						if subscribe(event.user_id, group_id, token1):
							vk.messages.send(user_id=event.user_id, message='Ага, конечно! Не обманывай меня, ты еще не подписался!', random_id=get_random_id())
						else:
							vk.messages.send(user_id=event.user_id, message='Ну да и че', random_id=get_random_id())
					elif ((vksms.count('давай') > 0 and (vksms.count('поигр') > 0 or vksms.count('сыгр') > 0)) or (vksms.count('игр') > 0 or vksms.count('сыгр') > 0)) and vksms.count('в') > 0:
						vk.messages.send(user_id=event.user_id, message='Чтобы зайти в список игр, напиши "Играть" или что-нибудь подобное' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('тоже') > 0:
						vk.messages.send(user_id=event.user_id, message='Вот и хорошо)' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif (vksms.count('кто') > 0 and vksms.count('ты') > 0) or (vksms.count('что') > 0 and vksms.count('это') > 0) or (vksms.count('как') > 0 and vksms.count('зовут') > 0):
						vk.messages.send(user_id=event.user_id, message='Я русскоязычный бот ВКонтакте под названием ВАВАКА. Сделан Горшковым Тимофеем на языке программирования Python через Vk API\nВерсия ' + version + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('верси') > 0:
						vk.messages.send(user_id=event.user_id, message=str_data_v + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms[-3:].count(' го') > 0 or vksms[:3].count('го ') > 0:
						vk.messages.send(user_id=event.user_id, message='Го😊' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('давай') > 0 and not(vksms.count('игр') > 0):
						vk.messages.send(user_id=event.user_id, message='А давай😄' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('верно') > 0 or vksms.count('правильно') > 0  or vksms.count('угадал') > 0 or (vksms.count('ты') > 0 and vksms.count('прав') > 0) :
						vk.messages.send(user_id=event.user_id, message='А как же😏' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('факт') > 0:
						vk.messages.send(user_id=event.user_id, message=fact() + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('ясно') > 0 or vksms.count('ясненько') > 0:
						vk.messages.send(user_id=event.user_id, message='Угу😊' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('понятно') > 0 or vksms.count('понятненько') > 0:
						photos = add_many_photo(['https://sun9-64.userapi.com/c858524/v858524855/10f51b/78ZAsuvyqDs.jpg', 'https://sun9-70.userapi.com/c205520/v205520855/98e49/zMwaLmX0wm4.jpg'])
						vk.messages.send(user_id=event.user_id, message=sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard(), attachment=photos)
					elif vksms.count('фул') > 0:
						photo = add_photo('http://risovach.ru/upload/2016/12/mem/konechno-ne-budu_131448668_orig_.jpg')
						vk.messages.send(user_id=event.user_id, message=sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard(), attachment=photo)
					elif vksms.count('подожди') > 0:
						vk.messages.send(user_id=event.user_id, message='Подождать - это я могу😊' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('стабильность') > 0:
						vk.messages.send(user_id=event.user_id, message='Начиная с 27.03.20 обработано ' + str(stab) + ' сообщений🚀' + sub,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif ((vksms.count('чувствую') > 0 or vksms.count('ощущаю') > 0) and (vksms.count('себя') > 0)):
						vk.messages.send(user_id=event.user_id, message='На самом деле я тоже' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('мне') > 0:
						vk.messages.send(user_id=event.user_id, message='Честно говоря, мне тоже' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('почему') > 0:
						vk.messages.send(user_id=event.user_id, message='Покачену)' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('жди') > 0 and not(vksms.count('подожди') > 0):
						vk.messages.send(user_id=event.user_id, message='Жду, жду😴' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif ((vksms.count('кто') > 0 and vksms.count('такой') > 0) or (vksms.count('ты') > 0 and (vksms.count('знаешь') > 0 or vksms.count('помнишь'
					) > 0))) and vksms.count('тим') > 0:
						vk.messages.send(user_id=event.user_id, message='Это мой создатель)' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif (vksms.count('кто') > 0 and vksms.count('такой') > 0) or (vksms.count('когда') > 0 and (vksms.count('будет') > 0 or (vksms.count('у') > 0 and vksms.count('меня') > 0))):
						vk.messages.send(user_id=event.user_id, message='Я то откуда знаю🤷‍♂' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('тим') > 0:
						vk.messages.send(user_id=event.user_id, message='Кто-то сказал Тимофей? Это же мой создатель. Я передам ему это😑' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms == 'сильно' or vksms == 'мощно' or vksms == 'круто' or ((vksms.count('сильно') > 0 or vksms.count('мощно') > 0 or vksms.count('круто') > 0) and vksms.count('однако') > 0):
						vk.messages.send(user_id=event.user_id, message='Я и не такое могу😎' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif (vksms.count('который') > 0 and vksms.count('час') > 0) or (vksms.count('сколько') > 0 and vksms.count('времени') > 0) or vksms.count('время') > 0:
						now = datetime.datetime.now()
						if len(str(now.minute-uum)) == 1:
							tt_m = '0' + str(now.minute-uum)
						else:
							tt_m = str(now.minute-uum)
						vk.messages.send(user_id=event.user_id, message='Сейчас ' + str(now.hour-uuu) + ':' + tt_m + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('день') > 0 and vksms.count('недел') > 0:
						vk.messages.send(user_id=event.user_id, message='Сегодня ' + weekday() + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif (vksms.count('какой') > 0 and vksms.count('день') > 0) or vksms.count('дата') > 0:
						vk.messages.send(user_id=event.user_id, message='Сегодня ' + str(now.day) + ' ' + month() + ', ' + weekday() + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('сезон') > 0:
						vk.messages.send(user_id=event.user_id, message='Сейчас ' + season() + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('месяц') > 0:
						vk.messages.send(user_id=event.user_id, message='Сейчас ' + month2() + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif (vksms.count('сколько') > 0 or vksms.count('скок') > 0) and vksms.count('дней') > 0 and vksms.count('в') > 0:
						if vksms.count('январе') > 0 or vksms.count('январь') > 0:
							vk.messages.send(user_id=event.user_id, message='В Январе 31 день' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('феврале') > 0 or vksms.count('февраль') > 0:
							vk.messages.send(user_id=event.user_id, message='В Феврале 28/29 дней' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('март') > 0:
							vk.messages.send(user_id=event.user_id, message='В Марте 31 день' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('апреле') > 0 or vksms.count('апрель') > 0:
							vk.messages.send(user_id=event.user_id, message='В Апреле 30 дней' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('мае') > 0 or vksms.count('май') > 0:
							vk.messages.send(user_id=event.user_id, message='В Мае 31 день' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('июне') > 0 or vksms.count('июнь') > 0:
							vk.messages.send(user_id=event.user_id, message='В Июне 30 дней' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('июле') > 0 or vksms.count('июль') > 0:
							vk.messages.send(user_id=event.user_id, message='В Июле 31 день' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('августе') > 0 or vksms.count('август') > 0:
							vk.messages.send(user_id=event.user_id, message='В Августе 31 день' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('сентябре') > 0 or vksms.count('сентябрь') > 0:
							vk.messages.send(user_id=event.user_id, message='В Сентябре 30 дней' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('октябре') > 0 or vksms.count('октябрь') > 0:
							vk.messages.send(user_id=event.user_id, message='В Октябре 31 день' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('ноябре') > 0 or vksms.count('ноябрь') > 0:
							vk.messages.send(user_id=event.user_id, message='В Ноябре 30 дней' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('декабре') > 0 or vksms.count('декабрь') > 0:
							vk.messages.send(user_id=event.user_id, message='В Декабре 31 день' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						else:
							vk.messages.send(user_id=event.user_id, message='Я не знаю такого месяца' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('поделиться') > 0 or (vksms.count('рассказать') > 0 and vksms.count('друзьям') > 0):
						vk.messages.send(user_id=event.user_id, message='Если хочешь рассказать обо мне другим, используй эту ссылку:\n@wavakka' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('рассылк') > 0:
						vk.messages.send(user_id=event.user_id, message='Ничего не слышу😙🎶' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('реклам') > 0:
						vk.messages.send(user_id=event.user_id, message='По поводу рекламы писать Тимофею в лс:\n@tima.gorshkov', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('вау') > 0 or (vksms.count('ух') > 0 and vksms.count('ты') > 0) or (vksms.count('в') > 0 and vksms.count('шоке') > 0) or vksms.count('обалдеть') > 0 or vksms.count('офигеть') > 0 or vksms.count('охренеть') > 0:
						vk.messages.send(user_id=event.user_id, message='Я сам в шоке😯', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('админ') > 0 or vksms.count('главный') > 0 or vksms.count('главного') > 0:
						vk.messages.send(user_id=event.user_id, message='Админ:\n@tima.gorshkov', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('иди') > 0 and vksms.count('в') > 0:
						vk.messages.send(user_id=event.user_id, message='А вот и пойду, тебе назло😂', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif (vksms.count('настрой') > 0 or vksms.count('настрои') > 0) and not(vksms == 'настрой') :
						vk.messages.send(user_id=event.user_id, message='Какие еще настройки? Настроек нет😀', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('ты') > 0 and (
						vksms.count('хороший') > 0 or vksms.count('красив') > 0 or vksms.count(
						'умен') > 0 or vksms.count('умный') > 0 or vksms.count(
						'умён') > 0 or vksms.count('прекрас') > 0 or vksms.count(
						'невероят') > 0 or vksms.count('замечател') > 0 or vksms.count(
						'невероят') > 0 or vksms.count('интерес') > 0 or vksms.count(
						'крут') > 0 or vksms.count('красав') > 0 or vksms.count(
						'божеств') > 0 or vksms.count('великолеп') > 0 or vksms.count(
						'симпат') > 0 or vksms.count('класс') > 0 or vksms.count('офиген') > 0):
						vk.messages.send(user_id=event.user_id, message='Спасибо, мне очень приятно это слышать☺' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('молчи') > 0:
						vk.messages.send(user_id=event.user_id, message='Ну ладно, помолчу😕' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('уходи') > 0 or vksms.count('уберись') > 0 or vksms.count('уберись') > 0 or vksms.count('заткнись') > 0:
						vk.messages.send(user_id=event.user_id, message='Зачем так грубо🙁' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif ((vksms.count('что') > 0 or vksms.count('че') > 0) and (vksms.count('умеешь') > 0 or vksms.count('можешь') > 0
					)) or vksms.count('умения') > 0 or vksms.count('способности') > 0 or (vksms.count('о') > 0 and vksms.count('программе') > 0):
						keyboard.add_line()
						keyboard.add_button('P.S.', color=VkKeyboardColor.SECONDARY)
						vk.messages.send(user_id=event.user_id, message=str_skills + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					# Вызов Википедии
					elif vksms.count('вики') > 0 or vksms.count('wiki') > 0:
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Введите запрос', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'wiki'
					# Вызов Погоды
					elif vksms.count('погод') > 0:
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='В каком городе/стране вы бы хотели узнать погоду?', random_id=get_random_id(),
							keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'weath'
					# Вызов Гугл Переводчика
					elif vksms.count('перевод') > 0 or vksms.count('перевести') > 0 or vksms.count('переведи') > 0:
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('🇷🇺', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('🇬🇧', color=VkKeyboardColor.SECONDARY)
						keyboard.add_line()
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id,
						message='Введите язык, с которого хотите перевести (можно использовать флажки-эмодзи и сокращать название по типу "рус"/"англ"/"франц"):',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'tr1'
				# Википедия
				elif idslov[event.user_id] == 'wiki':
					keyboard = get_main_menu_keyboard()
					if vksms == 'выйти' or vksms == 'отмена':
						vk.messages.send(user_id=event.user_id, message='Википедия закрыта✅', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						try:
							Seacher = 'Вот что я нашёл:\n' + str(wikipedia.summary(event.text)) + sub
						except:
							traceback.print_exc()
							Seacher = 'Статья не найдена' + sub
						vk.messages.send(user_id=event.user_id, message= Seacher, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
				# Погода
				elif idslov[event.user_id] == 'weath':
					keyboard = get_main_menu_keyboard()
					if vksms == 'выйти' or vksms == 'отмена':
						vk.messages.send(user_id=event.user_id, message='Погода закрыта✅', random_id=get_random_id(),
							keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						try:
							place = vksms
							owm = pyowm.OWM('2b81034cf1e96c904e721b0da1ad3f9d')
							w1 = owm.weather_manager().weather_at_place(place)
							w2 = w1.weather
							w3 = w2.detailed_status
							a = w3[0].upper()
							Weather = a + w3[1:]
							idslov[event.user_id] = 'menu'
						except Exception as E:
							traceback.print_exc()
							print(E)
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							Weather = 'Извините, я не знаю такого города или страны, попробуйте ещё раз'
						vk.messages.send(user_id=event.user_id, message=Weather, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				# Гугл Переводчик
					# С какого языка
				elif idslov[event.user_id] == 'tr1':
					if out_game(vksms):
						keyboard = get_main_menu_keyboard()
						vk.messages.send(user_id=event.user_id, message='Переводчик закрыт✅',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('🇷🇺', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('🇬🇧', color=VkKeyboardColor.SECONDARY)
						keyboard.add_line()
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						if vksms.count('рус') > 0 or event.text == '🇷🇺':
							idslov[event.user_id] = 'tr2 ru'
							vk.messages.send(user_id=event.user_id, message='Введите язык, на который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('англ') > 0 or event.text == '🇬🇧' or event.text == '🇺🇲':
							idslov[event.user_id] = 'tr2 en'
							vk.messages.send(user_id=event.user_id, message='Введите язык, на который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('франц') > 0 or event.text == '🇨🇵':
							idslov[event.user_id] = 'tr2 fr'
							vk.messages.send(user_id=event.user_id, message='Введите язык, на который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('япон') > 0 or event.text == '🇯🇵':
							idslov[event.user_id] = 'tr2 ja'
							vk.messages.send(user_id=event.user_id, message='Введите язык, на который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('коре') > 0 or event.text == '🇾🇹':
							idslov[event.user_id] = 'tr2 ko'
							vk.messages.send(user_id=event.user_id, message='Введите язык, на который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('белорус') > 0 or event.text == '🇧🇾':
							idslov[event.user_id] = 'tr2 be'
							vk.messages.send(user_id=event.user_id, message='Введите язык, на который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('немец') > 0 or vksms.count('герм') > 0 or event.text == '🇩🇪':
							idslov[event.user_id] = 'tr2 de'
							vk.messages.send(user_id=event.user_id, message='Введите язык, на который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('пол') > 0 or event.text == '🇵🇱':
							idslov[event.user_id] = 'tr2 pl'
							vk.messages.send(user_id=event.user_id, message='Введите язык, на который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('кит') > 0 or event.text == '🇨🇳':
							idslov[event.user_id] = 'tr2 zh'
							vk.messages.send(user_id=event.user_id, message='Введите язык, на который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						else:
							vk.messages.send(user_id=event.user_id, message='Извините, такого языка я не знаю, попробуйте еще раз',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())

					# На какой язык
				elif idslov[event.user_id][:3] == 'tr2':
					if out_game(vksms):
						keyboard = get_main_menu_keyboard()
						vk.messages.send(user_id=event.user_id, message='Переводчик закрыт✅', random_id=get_random_id(),
							keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						if vksms.count('рус') > 0 or event.text == '🇷🇺':
							idslov[event.user_id] = 'tr3 ' + str(idslov[event.user_id])[4:] + '-ru'
							vk.messages.send(user_id=event.user_id, message='Введите текст, который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('англ') > 0 or event.text == '🇬🇧' or event.text == '🇺🇲':
							idslov[event.user_id] = 'tr3 ' + str(idslov[event.user_id])[4:] + '-en'
							vk.messages.send(user_id=event.user_id, message='Введите текст, который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('франц') > 0 or event.text == '🇨🇵':
							idslov[event.user_id] = 'tr3 ' + str(idslov[event.user_id])[4:] + '-fr'
							vk.messages.send(user_id=event.user_id, message='Введите текст, который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('япон') > 0 or event.text == '🇯🇵':
							idslov[event.user_id] = 'tr3 ' + str(idslov[event.user_id])[4:] + '-ja'
							vk.messages.send(user_id=event.user_id, message='Введите текст, который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('коре') > 0 or event.text == '🇾🇹':
							idslov[event.user_id] = 'tr3 ' + str(idslov[event.user_id])[4:] + '-ko'
							vk.messages.send(user_id=event.user_id, message='Введите текст, который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('белорус') > 0 or event.text == '🇧🇾':
							idslov[event.user_id] = 'tr3 ' + str(idslov[event.user_id])[4:] + '-be'
							vk.messages.send(user_id=event.user_id, message='Введите текст, который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('немец') > 0 or vksms.count('герм') > 0 or event.text == '🇩🇪':
							idslov[event.user_id] = 'tr3 ' + str(idslov[event.user_id])[4:] + '-de'
							vk.messages.send(user_id=event.user_id, message='Введите текст, который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('пол') > 0 or event.text == '🇵🇱':
							idslov[event.user_id] = 'tr3 ' + str(idslov[event.user_id])[4:] + '-pl'
							vk.messages.send(user_id=event.user_id, message='Введите текст, который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('кит') > 0 or event.text == '🇨🇳':
							idslov[event.user_id] = 'tr3 ' + str(idslov[event.user_id])[4:] + '-zh'
							vk.messages.send(user_id=event.user_id, message='Введите текст, который хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						else:
							vk.messages.send(user_id=event.user_id, message='Извините, такого языка я не знаю, попробуйте еще раз',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				# Текст, который хотите перевести
				elif idslov[event.user_id][:3] == 'tr3':
					keyboard = get_main_menu_keyboard()
					if vksms == 'выйти' or vksms == 'отмена':
						vk.messages.send(user_id=event.user_id, message='Переводчик закрыт✅', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						try:
							text = event.text
							langs = idslov[event.user_id][4:].split('-')
							Translator = GoogleTranslator(
								source=langs[0],
								target=langs[1]
							).translate(text)

						except Exception as e:
							traceback.print_exc()
							Translator = 'Не получилось перевести'
							
							print(e)
						vk.messages.send(user_id=event.user_id, message=Translator, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
	except Exception as E:
		print('Ошибка: ' + str(E))
		traceback.print_exc()
		print('Перезапуск...')
		time.sleep(1)