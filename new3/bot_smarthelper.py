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
import string

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
token1 = 'vk1.a.s0D4LCy7W8GVc-zXS7b7Ji4Y9lt_n9aNBSzwWMr5kibY-Opy_me0MPx_C6etk54nUIMqdXJfFxwvBt5VUXxaril4qPHYl6-uAP2vey-qhmULf90vQxDowW6ljDKqCuUJfVPZCRcKbCNc7kuV1qJlBztkf5vaLzedQCbhOQC1mOoC-iB_yMYjAPY4bGH3rNS8_sWRH-KeDqPpTTERyUI0sQ'
group_id = '236395278'
vk_session = vk_api.VkApi(token=token1)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
# Некоторые переменные:
sub = ''
version = '2.3'
str_skills = 'Я бот - умный помощник. Авторы: Горшков Тимофей, Мендыгалиев Данияр, Барсуков Максим (2026 г.). Вот, что я умею:' \
			 '\n⭐ Напиши "переводчик морзе", "перевод морзе", "морзе", "морзянка" и т.д., чтобы перевести текст в морзянку и обратно' \
			 '\n⭐ Напиши "курс доллара", "курс евро" и т.д., чтобы узнать курс той или иной валюты к рублю (чтобы узнать, какие валюты доступны, напиши "валюты")'\
			 '\n⭐ Напиши "калькулятор валют", чтобы перевести количество одной валюты в другую'\
			 '\n⭐ Напиши "пароль", чтобы сгенерировать рандомный пароль'\
			 '\n⭐ Напиши "стабильность", чтобы узнать, сколько бот отправил сообщений, начиная с 4.03.26' \
			 '\n⭐ Напиши "график", чтобы посмотреть график доллара по заданной дате'\
             '\n🔆 А вообще можешь просто со мной поболтать😄'
str_data_v = 'Версия ' + version + '\nДаты других версий: ' \
								   '\n"test_group", "bot_tima" - 1.0 (17.02.2020)' \
								   '\n"Wavaka" - 2.0 (23.02.20)' \
								   '\n"Wavaka" - 2.1 (8.03.20)' \
								   '\n"Wavaka" - 2.2 (27.03.20)' \
								   '\n"Wavaka" - 2.3 (22.04.20)'
str_value = 'Вот все доступные мне валюты:' \
			'\n🇷🇺Рубль (RUB)' \
			'\n🇺🇸Доллар США (USD)' \
			'\n🇪🇺Евро (EUR)' \
			'\n🇨🇭Швейцарский франк (CHF)' \
			'\n🇬🇧Фунт стерлингов (GBP)' \
			'\n🇯🇵Иена (JPY)' \
			'\n🇰🇿Казахстанский тенге (KZT)' \
			'\n🇧🇾Белорусский рубль (BYN)' \
			'\n🇹🇷Турецкая лира (TRY)' \
			'\n🇨🇳Китайский юань (CNY)' \
			'\n🇦🇺Австралийский доллар (AUD)' \
			'\n🇨🇦Канадский доллар (CAD)' \
			'\n🇵🇱Польский злотый (PLN)' \
			'\n🇰🇷Южнокорейская вона (KRW)' \
			'\n➡Чтобы вызвать функцию курса валют, напиши "курс доллара", "валюта 🇺🇸", "валюта USD" и т.д.' \
			'\n➡Чтобы узнать состояние всех валют, напиши "курс всех валют"'
# Функции:
def get_main_menu_keyboard():
	keyboard = VkKeyboard(one_time=True)
	keyboard.add_button('Морзе', color=VkKeyboardColor.PRIMARY)
	keyboard.add_button('О программе', color=VkKeyboardColor.POSITIVE)
	keyboard.add_line()
	keyboard.add_button('Калькулятор валют', color=VkKeyboardColor.SECONDARY)
	keyboard.add_line()
	keyboard.add_button('Курс евро', color=VkKeyboardColor.SECONDARY)
	keyboard.add_button('Пароль', color=VkKeyboardColor.SECONDARY)
	keyboard.add_line()
	keyboard.add_button('Валюты', color=VkKeyboardColor.SECONDARY)
	keyboard.add_button('График', color=VkKeyboardColor.SECONDARY)
	return keyboard

def password(length=10):
    if length < 8:
        length = 8
    
    # Берем по одному символу каждого типа для гарантии
    password_chars = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]
    
    # Добавляем остальные случайные символы
    all_chars = string.ascii_letters + string.digits + string.punctuation
    for _ in range(length - 4):
        password_chars.append(random.choice(all_chars))
    
    # Перемешиваем, чтобы первые символы не были предсказуемыми
    random.shuffle(password_chars)
    return ''.join(password_chars)

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

def v_morze(sms): # Кодирование в морзе
	rash = ''
	for i in sms:
		if i == ' ':
			rash += ' / '
		elif i == 'а' or i == 'А':
			rash += '._'
		elif i == 'б' or i == 'Б':
			rash += '_...'
		elif i == 'в' or i == 'В':
			rash += '.__'
		elif i == 'г' or i == 'Г':
			rash += '__.'
		elif i == 'д' or i == 'Д':
			rash += '_..'
		elif i == 'е' or i == 'Е':
			rash += '.'
		elif i == 'ё' or i == 'Ё':
			rash += '.'
		elif i == 'ж' or i == 'Ж':
			rash += '..._'
		elif i == 'з' or i == 'З':
			rash += '__..'
		elif i == 'и' or i == 'И':
			rash += '..'
		elif i == 'й' or i == 'Й':
			rash += '.___'
		elif i == 'к' or i == 'К':
			rash += '_._'
		elif i == 'л' or i == 'Л':
			rash += '._..'
		elif i == 'м' or i == 'М':
			rash += '__'
		elif i == 'н' or i == 'Н':
			rash += '_.'
		elif i == 'о' or i == 'О':
			rash += '___'
		elif i == 'п' or i == 'П':
			rash += '.__.'
		elif i == 'р' or i == 'Р':
			rash += '._.'
		elif i == 'с' or i == 'С':
			rash += '...'
		elif i == 'т' or i == 'Т':
			rash += '_'
		elif i == 'у' or i == 'У':
			rash += '.._'
		elif i == 'ф' or i == 'Ф':
			rash += '.._.'
		elif i == 'х' or i == 'Х':
			rash += '....'
		elif i == 'ц' or i == 'Ц':
			rash += '_._.'
		elif i == 'ч' or i == 'Ч':
			rash += '___.'
		elif i == 'ш' or i == 'Ш':
			rash += '____'
		elif i == 'щ' or i == 'Щ':
			rash += '__._'
		elif i == 'ъ' or i == 'Ъ':
			rash += '.__._.'
		elif i == 'ы' or i == 'Ы':
			rash += '_.__'
		elif i == 'ь' or i == 'Ь':
			rash += '_.._'
		elif i == 'э' or i == 'Э':
			rash += '.._..'
		elif i == 'ю' or i == 'Ю':
			rash += '..__'
		elif i == 'я' or i == 'Я':
			rash += '._._'
		elif i == '.':
			rash += '......'
		elif i == ',':
			rash += '._._._'
		elif i == ':':
			rash += '___...'
		elif i == ';':
			rash += '_._._.'
		elif i == '(' or i == ')':
			rash += '_.__._'
		elif i == '?':
			rash += '..__..'
		elif i == '!':
			rash += '__..__'
		elif i == "'" or i == '"':
			rash += '._.._.'
		elif i == '0':
			rash += '_____'
		elif i == '1':
			rash += '.____'
		elif i == '2':
			rash += '..___'
		elif i == '3':
			rash += '...__'
		elif i == '4':
			rash += '...._'
		elif i == '5':
			rash += '.....'
		elif i == '6':
			rash += '_....'
		elif i == '7':
			rash += '__...'
		elif i == '8':
			rash += '___..'
		elif i == '9':
			rash += '____.'
		else:
			return 'Ошибка'
		rash += ' '
	return rash
def iz_morze(sms): # Кодирование из морзе
	sms = sms.split()
	rash = ''
	if sms.count('*') > 0:
		sms = sms.replace('*', '.')
	if sms.count('-') > 0:
		sms = sms.replace('-', '_')
	if sms.count('—') > 0:
		sms = sms.replace('—', '_')
	if sms.count('—') > 0:
		sms = sms.replace('—', '_')
	for i in sms:
		if i == ' ':
			rash += ''
		if i == '  ':
			rash += ' '
		elif i == '._':
			rash += 'а'
		elif i == '_...':
			rash += 'б'
		elif i == '.__':
			rash += 'в'
		elif i == '__.':
			rash += 'г'
		elif i == '_..':
			rash += 'д'
		elif i == '.':
			rash += 'е'
		elif i == '..._':
			rash += 'ж'
		elif i == '__..':
			rash += 'з'
		elif i == '..':
			rash += 'и'
		elif i == '.___':
			rash += 'й'
		elif i == '_._':
			rash += 'к'
		elif i == '._..':
			rash += 'л'
		elif i == '__':
			rash += 'м'
		elif i == '_.':
			rash += 'н'
		elif i == '..':
			rash += 'и'
		elif i == '___':
			rash += 'о'
		elif i == '.__.':
			rash += 'п'
		elif i == '._.':
			rash += 'р'
		elif i == '...':
			rash += 'с'
		elif i == '_':
			rash += 'т'
		elif i == '.._':
			rash += 'у'
		elif i == '.._.':
			rash += 'ф'
		elif i == '....':
			rash += 'х'
		elif i == '_._.':
			rash += 'ц'
		elif i == '___.':
			rash += 'ч'
		elif i == '____':
			rash += 'ш'
		elif i == '__._':
			rash += 'щ'
		elif i == '.__._.':
			rash += 'ъ'
		elif i == '_.__':
			rash += 'ы'
		elif i == '_.._':
			rash += 'ь'
		elif i == '.._..':
			rash += 'э'
		elif i == '..__':
			rash += 'ю'
		elif i == '._._':
			rash += 'я'
		elif i == '......':
			rash += '.'
		elif i == '._._._':
			rash += ','
		elif i == '___...':
			rash += ':'
		elif i == '_._._.':
			rash += ';'
		elif i == '_.__._':
			rash += '('
		elif i == '..__..':
			rash += '?'
		elif i == '__..__':
			rash += '!'
		elif i == "._.._.":
			rash += '"'
		elif i == '_____':
			rash += '0'
		elif i == '.____':
			rash += '1'
		elif i == '..___':
			rash += '2'
		elif i == '...__':
			rash += '3'
		elif i == '...._':
			rash += '4'
		elif i == '.....':
			rash += '5'
		elif i == '_....':
			rash += '6'
		elif i == '__...':
			rash += '7'
		elif i == '___..':
			rash += '8'
		elif i == '____.':
			rash += '9'
		else:
			return 'Ошибка'
	return rash

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
def randcow(c): # Случайное число для игры "Быки и коровы"
	l = list(range(0, 9))
	ss = ''
	random.shuffle(l)
	for i in range(c):
		if l[i] == 0 and i == 0:
			ss += str(l[8])
		else:
			ss += str(l[i])
	return ss
def out_game(t):
	if t == 'отмена' or t == 'выйти' or t == 'закончить' or t == 'прекратить'  or t == 'хватит' or t == 'достаточно' or t == 'назад' or t == 'вернуться':
		return True
	else:
		return False

def help_value(fr, c):
	c = int(c)
	if fr == 'RUB':
		if c == float(c):
			if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
				return 'рублей 🇷🇺'
			elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
				return 'рубля 🇷🇺'
			elif c == 1 or c % 10 >= 1 and c > 10:
				return 'рубль 🇷🇺'
			else:
				return 'рублей 🇷🇺'
		else:
			return 'рубля 🇷🇺'
	elif fr == 'USD':
		if c == float(c):
			if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
				return 'долларов 🇺🇸'
			elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
				return 'доллара 🇺🇸'
			elif c == 1 or c % 10 >= 1 and c > 10:
				return 'доллар 🇺🇸'
			else:
				return 'долларов 🇺🇸'
		else:
			return 'доллара 🇺🇸'
	elif fr == 'EUR':
		return 'евро 🇪🇺'
	elif fr == 'CHF':
		if c == float(c):
			if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
				return 'швейцарских франков 🇨🇭'
			elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
				return 'швейцарских франка 🇨🇭'
			elif c == 1 or c % 10 >= 1 and c > 10:
				return 'швейцарский франк 🇨🇭'
			else:
				return 'швейцарских франков 🇨🇭'
		else:
			return 'швейцарских франка 🇨🇭'
	elif fr == 'GBP':
		if c == float(c):
			if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
				return 'фунтов стерлингов 🇬🇧'
			elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
				return 'фунта стерлингов 🇬🇧'
			elif c == 1 or c % 10 >= 1 and c > 10:
				return 'фунт стерлингов 🇬🇧'
			else:
				return 'фунтов стерлингов 🇬🇧'
		else:
			return 'фунта стерлингов 🇬🇧'
	elif fr == 'JPY':
		if c == float(c):
			if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
				return 'иен 🇯🇵'
			elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
				return 'иены 🇯🇵'
			elif c == 1 or c % 10 >= 1 and c > 10:
				return 'иена 🇯🇵'
			else:
				return 'иен 🇯🇵'
		else:
			return 'иены 🇯🇵'
	elif fr == 'KZT':
		if c == float(c):
			if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
				return 'казахстанских тенге 🇰🇿'
			elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
				return 'казахстанских тенге 🇰🇿'
			elif c == 1 or c % 10 >= 1 and c > 10:
				return 'казахстанский тенге 🇰🇿'
			else:
				return 'казахстанских тенге 🇰🇿'
		else:
			return 'казахстанских тенге 🇰🇿'
	elif fr == 'BYN':
		if c == float(c):
			if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
				return 'белорусских рублей 🇧🇾'
			elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
				return 'белорусского рубля 🇧🇾'
			elif c == 1 or c % 10 >= 1 and c > 10:
				return 'белорусский рубль 🇧🇾'
			else:
				return 'белорусских рублей 🇧🇾'
		else:
			return 'белорусского рубля 🇧🇾'
	elif fr == 'TRY':
		if c == float(c):
			if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
				return 'турецкой лиры 🇹🇷'
			elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
				return 'турецкой лиры 🇹🇷'
			elif c == 1 or c % 10 >= 1 and c > 10:
				return 'турецкая лира 🇹🇷'
			else:
				return 'турецкой лиры 🇹🇷'
		else:
			return 'турецкой лиры 🇹🇷'
	elif fr == 'CNY':
		if c == float(c):
			if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
				return 'китайских юаней 🇨🇳'
			elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
				return  'китайского юаня 🇨🇳'
			elif c == 1 or c % 10 >= 1 and c > 10:
				return 'китайский юань 🇨🇳'
			else:
				return 'китайских юаней 🇨🇳'
		else:
			return 'китайского юаня 🇨🇳'
	elif fr == 'AUD':
		if c == float(c):
			if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
				return  'австралийских долларов 🇦🇺'
			elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
				return  'австралийских доллара 🇦🇺'
			elif c == 1 or c % 10 >= 1 and c > 10:
				return  'австралийский доллар 🇦🇺'
			else:
				return  'австралийских долларов 🇦🇺'
		else:
			return 'австралийских доллара 🇦🇺'
	elif fr == 'CAD':
		if c == float(c):
			if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
				return  'канадских долларов 🇨🇦'
			elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
				return  'канадских доллара 🇨🇦'
			elif c == 1 or c % 10 >= 1 and c > 10:
				return  'канадский доллар 🇨🇦'
			else:
				return  'канадских долларов 🇨🇦'
		else:
			return 'канадских доллара 🇨🇦'
	elif fr == 'PLN':
		if c == float(c):
			if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
				return  'польских злотых 🇵🇱'
			elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
				return  'польского злотого 🇵🇱'
			elif c == 1 or c % 10 >= 1 and c > 10:
				return  'польский злотый 🇵🇱'
			else:
				return  'польских злотых 🇵🇱'
		else:
			return 'польского злотого 🇵🇱'
	elif fr == 'KRW':
		if c == float(c):
			if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
				return  'южнокорейских вон 🇰🇷'
			elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
				return  'южнокорейских воны 🇰🇷'
			elif c == 1 or c % 10 >= 1 and c > 10:
				return  'южнокорейская вона 🇰🇷'
			else:
				return  'южнокорейских вон 🇰🇷'
		else:
			return 'южнокорейских воны 🇰🇷'
	else:
		return ' '
def calculator_of_currencies(text): #(с какой валюты)-(на какую валюту)_(сколько) --- Пример: 4 доллара в рублях = 'usd-rub_4'
	#Узнаем курс валют
	now = str(datetime.datetime.now())
	aa = now.find(' ')
	data = now[:aa]
	rates = ExchangeRates(data)
	#Узнаем, что нам дали в тексте
	a = text.find('-')
	b = text.find('_')
	from_v = text[:a].upper()
	to_v = text[a+1:b].upper()
	count = float(text[b+1:])
	#Делаем from_c
	if from_v == 'RUB':
		from_c = 1
	else:
		from_c = rates[from_v].value
	if from_v == 'JPY' or from_v == 'KZT':
		from_c = from_c / 100
	elif from_v == 'UAH' or from_v == 'CNY':
		from_c = from_c / 10
	#Делаем to_c
	if to_v == 'RUB':
		to_c = 1
	else:
		to_c = rates[to_v].value
	if to_v == 'JPY' or to_v == 'KZT':
		to_c = to_c / 100
	elif to_v == 'UAH' or to_v == 'CNY':
		to_c = to_c / 10
	#Формула
	l1 = float(from_c)
	l2 = float(to_c)
	a = str(l1*count/l2)
	#Сокращаем до первых двух знаков после запятой
	b = a.find('.')
	equally = str(a[:b] + a[b:][:3])
	c1 = float(equally)
	c2 = int(c1)
	#Если после запятой нолик, просто ничего не пишем
	if int(str(count).split('.')[1]) == 0:
		count = int(count)
	if int(str(c1).split('.')[1]) == 0:
		equally = int(c1)

	word1 = help_value(from_v, count)
	word2 = help_value(to_v, c2)
	answer = str(count) + ' ' + word1 + ' = ' + str(equally) + ' ' + word2
	return answer

def glitch(num):
	str = '1234567890@₽_&-+()/\*"' + "'" + ':;!?¿‽¡‹›‚‚†···{}£€$¢^↑°∞≠≈=¶∆§π`~|✓[]%<>'
	list = []
	for i in str:
		list.append(i)
	random.shuffle(list)
	answer = ''
	for i in range(num):
		if i>=len(list)-1:
			random.shuffle(list)
			while i>=len(list)-1:
				i-=64
		answer+=list[i]
	return answer
def word_glitch(text):
	list = []
	for i in text:
		c = random.randint(1, 2)
		if c == 1:
			list.append(i.upper())
		elif c == 2:
			list.append(i.lower())
	answer = ''
	answer+=glitch(random.randint(0, 2))

	for i in list:
		if i == ' ':
			answer+='  '
			answer += glitch(random.randint(0, 2))
		else:
			gli = glitch(random.randint(0, 3))
			answer+= i + gli

	return answer
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
					# Вызов пароля
					elif vksms.count('пароль') > 0:
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Введите количество символов:', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'password'
					# Вызов калькулятор валют
					elif vksms.count('калькулятор') > 0 and vksms.count('валют') > 0:
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('🇷🇺', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('🇺🇸', color=VkKeyboardColor.SECONDARY)
						keyboard.add_line()
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Введите валюту, с которой хотите перевести:',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'calc'
					#Вызов валюты
					elif vksms == 'валюты' or vksms == 'все валюты':
						vk.messages.send(user_id=event.user_id, message=str_value + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('валют') > 0 or vksms.count('курс') > 0:
						now = str(datetime.datetime.now())
						aa = now.find(' ')
						data = now[:aa]
						rates = ExchangeRates(data)
						if vksms.count('евро') > 0 or vksms.count('eur') > 0 or vksms.count('🇪🇺') > 0:
							EUR1 = str(rates['EUR'].value)[:5]
							c = int(float(EUR1))
							if c == float(EUR1):
								EUR1 = str(int(EUR1))
								if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
									paste = ' рублей'
								elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
									paste = ' рубля'
								elif c == 1 or c % 10 >= 1 and c > 10:
									paste = ' рубль'
								else:
									paste = ' рублей'
							else:
								paste = ' рубля'
							vk.messages.send(user_id=event.user_id, message='🇪🇺Курс евро:\n1 евро = ' + EUR1 + paste + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('франк') > 0 or vksms.count('chf') > 0 or vksms.count('🇨🇭') > 0:
							CHF1 = str(rates['CHF'].value)[:5]
							c = int(float(CHF1))
							if c == float(CHF1):
								CHF1 = str(int(CHF1))
								if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
									paste = ' рублей'
								elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
									paste = ' рубля'
								elif c == 1 or c % 10 >= 1 and c > 10:
									paste = ' рубль'
								else:
									paste = ' рублей'
							else:
								paste = ' рубля'
							vk.messages.send(user_id=event.user_id, message='🇨🇭Курс швейцарского франка:\n1 франк = ' + CHF1 + paste + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('фунт') > 0 or vksms.count('стерлинг') > 0 or vksms.count('gbp') > 0 or vksms.count('🇬🇧') > 0:
							GBP1 = str(rates['GBP'].value)[:5]
							c = int(float(GBP1))
							if c == float(GBP1):
								GBP1 = str(int(GBP1))
								if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
									paste = ' рублей'
								elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
									paste = ' рубля'
								elif c == 1 or c % 10 >= 1 and c > 10:
									paste = ' рубль'
								else:
									paste = ' рублей'
							else:
								paste = ' рубля'
							vk.messages.send(user_id=event.user_id,message='🇬🇧Курс фунта стерлингов:\n1 фунт стерлинга = ' + GBP1 + paste + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('иена') > 0 or vksms.count('иены') > 0 or vksms.count('jpy') > 0 or vksms.count('🇯🇵') > 0:
							JPY100 = str(rates['JPY'].value)[:5]
							c = int(float(JPY100))
							if c == float(JPY100):
								JPY100 = str(int(JPY100))
								if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
									paste = ' рублей'
								elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
									paste = ' рубля'
								elif c == 1 or c % 10 >= 1 and c > 10:
									paste = ' рубль'
								else:
									paste = ' рублей'
							else:
								paste = ' рубля'
							vk.messages.send(user_id=event.user_id, message='🇯🇵Курс иены:\n100 иен = ' + JPY100 + paste + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('казахст') > 0 or vksms.count('тенге') > 0 or vksms.count('kzt') > 0 or vksms.count('🇰🇿') > 0:
							KZT100 = str(rates['KZT'].value)[:5]
							c = int(float(KZT100))
							if c == float(KZT100):
								KZT100 = str(int(KZT100))
								if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
									paste = ' рублей'
								elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
									paste = ' рубля'
								elif c == 1 or c % 10 >= 1 and c > 10:
									paste = ' рубль'
								else:
									paste = ' рублей'
							else:
								paste = ' рубля'
							vk.messages.send(user_id=event.user_id, message='🇰🇿Курс казахстанского тенге:\n100 тенге = ' + KZT100 + paste + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif (vksms.count('белорус') > 0 and vksms.count('рубл') > 0) or vksms.count('белорус') > 0 or vksms.count('byn') > 0 or vksms.count('🇧🇾') > 0:
							BYN1 = str(rates['BYN'].value)[:5]
							c = int(float(BYN1))
							if c == float(BYN1):
								BYN1 = str(int(BYN1))
								if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
									paste = ' рублей'
								elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
									paste = ' рубля'
								elif c == 1 or c % 10 >= 1 and c > 10:
									paste = ' рубль'
								else:
									paste = ' рублей'
							else:
								paste = ' рубля'
							vk.messages.send(user_id=event.user_id, message='🇧🇾Курс белорусского рубля:\n1 белорусский рубль = ' + BYN1 + paste + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('турец') > 0 or vksms.count('лиры') > 0 or vksms.count('лира') > 0 or vksms.count('try') > 0 or vksms.count('🇹🇷') > 0:
							TRY1 = str(rates['TRY'].value)[:5]
							c = int(float(TRY1))
							if c == float(TRY1):
								TRY1 = str(int(TRY1))
								if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
									paste = ' рублей'
								elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
									paste = ' рубля'
								elif c == 1 or c % 10 >= 1 and c > 10:
									paste = ' рубль'
								else:
									paste = ' рублей'
							else:
								paste = ' рубля'
							vk.messages.send(user_id=event.user_id, message='🇹🇷Курс турецкой лиры:\n1 лира = ' + TRY1 + paste + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('китай') > 0 or vksms.count('юань') > 0 or vksms.count('юаня') > 0 or vksms.count('cny') > 0 or vksms.count('🇨🇳') > 0:
							CNY10 = str(rates['CNY'].value)[:5]
							c = int(float(CNY10))
							if c == float(CNY10):
								CNY10 = str(int(CNY10))
								if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
									paste = ' рублей'
								elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
									paste = ' рубля'
								elif c == 1 or c % 10 >= 1 and c > 10:
									paste = ' рубль'
								else:
									paste = ' рублей'
							else:
								paste = ' рубля'
							vk.messages.send(user_id=event.user_id, message='🇨🇳Курс китайского юаня:\n10 юаней = ' + CNY10 + paste + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif (vksms.count('австрал') > 0 and vksms.count('доллар') > 0) or vksms.count('австрал') > 0 or vksms.count('aud') > 0 or vksms.count('🇦🇺') > 0:
							AUD1 = str(rates['AUD'].value)[:5]
							c = int(float(AUD1))
							if c == float(AUD1):
								AUD1 = str(int(AUD1))
								if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
									paste = ' рублей'
								elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
									paste = ' рубля'
								elif c == 1 or c % 10 >= 1 and c > 10:
									paste = ' рубль'
								else:
									paste = ' рублей'
							else:
								paste = ' рубля'
							vk.messages.send(user_id=event.user_id, message='🇦🇺Курс австралийский доллар:\n1 австралийский доллар = ' + AUD1 + paste + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif (vksms.count('канад') > 0 and vksms.count('доллар') > 0) or vksms.count('канад') > 0 or vksms.count('cad') > 0 or vksms.count('🇨🇦') > 0:
							CAD1 = str(rates['CAD'].value)[:5]
							c = int(float(CAD1))
							if c == float(CAD1):
								CAD1 = str(int(CAD1))
								if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
									paste = ' рублей'
								elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
									paste = ' рубля'
								elif c == 1 or c % 10 >= 1 and c > 10:
									paste = ' рубль'
								else:
									paste = ' рублей'
							else:
								paste = ' рубля'
							vk.messages.send(user_id=event.user_id, message='🇨🇦Курс канадского доллара:\n1 канадский доллар = ' + CAD1 + paste + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('польш') > 0 or vksms.count('польск') > 0 or vksms.count('злотый') > 0 or vksms.count('pln') > 0 or vksms.count('🇵🇱') > 0:
							PLN1 = str(rates['PLN'].value)[:5]
							c = int(float(PLN1))
							if c == float(PLN1):
								PLN1 = str(int(PLN1))
								if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
									paste = ' рублей'
								elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
									paste = ' рубля'
								elif c == 1 or c % 10 >= 1 and c > 10:
									paste = ' рубль'
								else:
									paste = ' рублей'
							else:
								paste = ' рубля'
							vk.messages.send(user_id=event.user_id, message='🇵🇱Курс польского злотого:\n1 польский злотый = ' + PLN1 + paste + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('корей') > 0 or vksms.count('корея') > 0 or vksms.count('вона') > 0 or vksms.count('krw') > 0 or vksms.count('🇰🇷') > 0:
							KRW1000 = str(rates['KRW'].value)[:5]
							c = int(float(KRW1000))
							if c == float(KRW1000):
								KRW1000 = str(int(KRW1000))
								if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
									paste = ' рублей'
								elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
									paste = ' рубля'
								elif c == 1 or c % 10 >= 1 and c > 10:
									paste = ' рубль'
								else:
									paste = ' рублей'
							else:
								paste = ' рубля'
							vk.messages.send(user_id=event.user_id, message='🇰🇷Курс южнокорейской воны:\n1000 южнокорейских вон = ' + KRW1000 + paste + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('рубл') > 0 or vksms.count('rub') > 0 or vksms.count('🇷🇺') > 0:
							vk.messages.send(user_id=event.user_id, message='🇷🇺Курс рубля:\n1 рубль = 1 рубль' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('доллар') > 0 or vksms.count('usd') > 0 or vksms.count('🇺🇸') > 0:
							USD1 = str(rates['USD'].value)[:5]
							c = int(float(USD1))
							if c == float(USD1):
								USD1 = str(int(USD1))
								if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
									paste = ' рублей'
								elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
									paste = ' рубля'
								elif c == 1 or c % 10 >= 1 and c > 10:
									paste = ' рубль'
								else:
									paste = ' рублей'
							else:
								paste = ' рубля'
							vk.messages.send(user_id=event.user_id, message='🇺🇸Курс доллара:\n1 доллар = ' + USD1 + paste + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('курс') > 0 and vksms.count('всех') > 0 and vksms.count('валют') > 0:
							USD1 = str(rates['USD'].value)[:5]
							EUR1 = str(rates['EUR'].value)[:5]
							CHF1 = str(rates['CHF'].value)[:5]
							GBP1 = str(rates['GBP'].value)[:5]
							JPY100 = str(rates['JPY'].value)[:5]
							UAH10 = str(rates['UAH'].value)[:5]
							KZT100 = str(rates['KZT'].value)[:5]
							BYN1 = str(rates['BYN'].value)[:5]
							TRY1 = str(rates['TRY'].value)[:5]
							CNY10 = str(rates['CNY'].value)[:5]
							AUD1 = str(rates['AUD'].value)[:5]
							CAD1 = str(rates['CAD'].value)[:5]
							PLN1 = str(rates['PLN'].value)[:5]
							KRW1000 = str(rates['KRW'].value)[:5]
							All_values = 'Состояние всех валют:' \
										 '\n🇷🇺Курс рубля:\n1 рубль = 1 рубль' \
										 '\n🇺🇸Курс доллара:\n1 доллар = ' + USD1 + ' рубля' \
										 '\n🇪🇺Курс евро:\n1 евро = ' + EUR1 + ' рубля' \
										 '\n🇨🇭Курс швейцарского франка:\n1 франк = ' + CHF1 + ' рубля' \
										 '\n🇬🇧Курс фунта стерлингов:\n1 фунт стерлинга = ' + GBP1 + ' рубля' \
										 '\n🇯🇵Курс иены:\n100 иен = ' + JPY100 + ' рубля' \
										 '\n🇰🇿Курс казахстанского тенге:\n100 тенге = ' + KZT100 + ' рубля' \
										 '\n🇧🇾Курс белорусского рубля:\n1 белорусский рубль = ' + BYN1 + ' рубля' \
										 '\n🇹🇷Курс турецкой лиры:\n1 лира = ' + TRY1 + ' рубля' \
										 '\n🇨🇳Курс китайского юаня:\n10 юаней = ' + CNY10 + ' рубля' \
										 '\n🇦🇺Курс австралийский доллар:\n1 австралийский доллар = ' + AUD1 + ' рубля' \
										 '\n🇨🇦Курс канадского доллара:\n1 канадский доллар = ' + CAD1 + ' рубля' \
										 '\n🇵🇱Курс польского злотого:\n1 польский злотый = ' + PLN1 + ' рубля' \
							             '\n🇰🇷Курс южнокорейской воны:\n1000 южнокорейских вон = ' + KRW1000 + ' рубля'
							vk.messages.send(user_id=event.user_id, message= All_values + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						else:
							vk.messages.send(user_id=event.user_id, message= 'Я не знаю такой валюты'+ sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					# Вызов графика доллара
					elif vksms.count('график') > 0:
						if not(file == 'C:\\Users\\Timofey\\Desktop\\idlist - vk_bot.txt'):
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Вы вошли в меню просмотра графика доллара по отношению к рублю', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
							vk.messages.send(user_id=event.user_id, message='Введите дату в формате 25.01.2020, С КОТОРОЙ вы хотите посмотреть график' , random_id=get_random_id(), keyboard=keyboard.get_keyboard())
							idslov[event.user_id] = 'chart'
						else:
							keyboard = get_main_menu_keyboard()
							vk.messages.send(user_id=event.user_id,message='К сожалению, просмотр графика доллара по отношению к рублю сейчас недоступен((',random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					# Вызов Морзе
					elif ((vksms.count('перевод') > 0 or vksms.count('перевести') > 0 or vksms.count('переведи') > 0) and vksms.count('морз') > 0) or vksms.count('морз') > 0:
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('1', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('2', color=VkKeyboardColor.SECONDARY)
						keyboard.add_line()
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id,
						message='Выберите команду:\n1 - Перевести из русского на морзе + справочник по Азбуке Морзе\n2 - Перевести из морзе на русский + справочник по Азбуке Морзе',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'morz'

				# График доллара
				elif idslov[event.user_id] == 'chart':
					if fhg == '1' or fhg == '3':
						if vksms == 'выйти' or vksms == 'отмена':
							keyboard = get_main_menu_keyboard()
							vk.messages.send(user_id=event.user_id, message='График доллара закрыт✅', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
							idslov[event.user_id] = 'menu'
						else:
							if len(event.text) == 10:
								keyboard = VkKeyboard(one_time=True)
								keyboard.add_button('Сегодня', color=VkKeyboardColor.SECONDARY)
								keyboard.add_line()
								keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
								vk.messages.send(user_id=event.user_id, message= 'Введите дату в формате 25.01.2020, ДО КОТОРОЙ вы хотите посмотреть график', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
								idslov[event.user_id] = 'chart ' + event.text
							else:
								keyboard = VkKeyboard(one_time=True)
								keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
								vk.messages.send(user_id=event.user_id, message='Неправильная запись даты. Повторяю: день.месяц.год', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					else:
						keyboard = get_main_menu_keyboard()
						vk.messages.send(user_id=event.user_id, message='Извини, но в данный момент просмотр графика доллара по отношению к рублю сейчас не доступен((', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
				elif idslov[event.user_id][:5] == 'chart':
					if vksms == 'выйти' or vksms == 'отмена':
						keyboard = get_main_menu_keyboard()
						vk.messages.send(user_id=event.user_id, message='График доллара закрыт✅', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						if len(event.text) == 10 or (vksms == 'сегодня' or vksms == 'сейчас'):
							data1 = idslov[event.user_id][6:]
							if vksms == 'сегодня' or vksms == 'сейчас':
								data2 = datetime.datetime.today().strftime('%d.%m.%Y')
							else:
								data2 = event.text
							vk.messages.send(user_id=event.user_id, message='Подождите, это может занять несколько секунд...', random_id=get_random_id())
							try:
								symbol = 'USD000UTSTOM'  # Тикер желаемого инструмента. В данном случае это доллар-рубль на валютном рынке Московской биржи.
								period = 8  # Период графика. 8 - это дневки. Один кирпичик данных описывает картину 1 дня: открытие, закрытие, максимум, минимум. Другие варианты: {'tick': 1, 'min': 2, '5min': 3, '10min': 4, '15min': 5, '30min': 6, 'hour': 7, 'daily': 8, 'week': 9, 'month': 10}
								start_date_str = data1  # с какой даты качаем данные
								end_date_str = data2  # по какую дату качаем данные. Здесь указано: "по сегодня"
								# выполняем преобразование дат, чтобы их понял Финам.
								start_date = datetime.datetime.strptime(start_date_str, "%d.%m.%Y").date()
								start_date_rev = datetime.datetime.strptime(start_date_str, '%d.%m.%Y').strftime('%Y%m%d')
								end_date = datetime.datetime.strptime(end_date_str, "%d.%m.%Y").date()
								end_date_rev = datetime.datetime.strptime(end_date_str, '%d.%m.%Y').strftime('%Y%m%d')
								# Все параметры упаковываем в единую структуру. Эти данные улетят от нас на Финам.
								# Как сделать тонкую настройку этого запроса, смотрите в моей статье на Смарт Лабе "Качаем котировки с Финама" https://smart-lab.ru/blog/514941.php
								params = urlencode([('market', 0), ('em', 182400), ('code', symbol), ('apply', 0),('df', start_date.day), ('mf', start_date.month - 1),('yf', start_date.year), ('from', start_date_str),('dt', end_date.day), ('mt', end_date.month - 1),('yt', end_date.year), ('to', end_date_str), ('p', period),('f', symbol + "_" + start_date_rev + "_" + end_date_rev),('e', ".csv"), ('cn', symbol), ('dtf', 1), ('tmf', 1), ('MSOR', 0),('mstime', "on"), ('mstimever', 1), ('sep', 1), ('sep2', 1),('datf', 1), ('at', 0)])
								# итоговый урл (строка), который улетит на сервер Финама:
								url = "http://export.finam.ru/" + symbol + "_" + start_date_rev + "_" + end_date_rev + ".csv?" + params
								txt = urlopen(url,
									timeout=10).readlines()  # На сайт Финама улетел урл. Оттуда прилетел ответ и записался в переменную txt
								x = []  # Здесь будут даты на горизонтальной оси.
								y = []  # Здесь будут цены на вертикальной оси.
								h = []
								for line in txt:  # бегаем в цикле по прилетевшим значениям. Разносим их по x и y
									tmp = str(line).split(",")  # читаем строчку за строчкой и выбираем из неё данные (значения разделены запятой)
									date = tmp[2]  # дата - это третье поле в строке
									h.append(date)
									x.append(matplotlib.dates.date2num(datetime.datetime.strptime(date, '%Y%m%d')))  # запишем дату в понятном для библиотеки matplotlib виде (она станет числом)
									y.append((float(tmp[5]) + float(tmp[6]) + float(tmp[7])) / 3)  # посчитаем типическую цену за день и добавим в chart_y. Типическая цена=(цена закрытия+максимум+минимум)/3.
								fig, ax = plt.subplots()  # начинаем работать с библиотекой matplotlib. Создаём фигуру.
								ymax = max(y)  # находим максимальное значение, до которого доходил доллар.
								xmax = x[y.index(ymax)]  # находим дату максимального значения.
								ymax = round(ymax, 2)  # округляем максимум до копеек.

								ax.annotate('MAX:' + str(ymax),
									# на график поместим аннотацию: максимальное значение доллара.
									xy=(xmax, ymax * (1.005)),
									# место куда поместим аннотацию: визуально чуть-чуть повыше максимума.
									horizontalalignment='center',  # выровняем метку максимума по центру.
											)
								ax.plot(x, y, color="g")  # наносим график доллара: оси x и y. Цвет зелёный.

								jack_date = ''
								if h[0][:4] == h[len(h) - 1][:4] and not (h[0][4:6] == h[len(h) - 1][4:6]):
									jack_date = '%d.%m'
									plt.title("USD/RUB, " + h[0][:4], fontsize=20)
								elif h[0][:4] == h[len(h) - 1][:4] and h[0][4:6] == h[len(h) - 1][4:6]:
									jack_date = '%d'
									plt.title("USD/RUB, " + h[0][4:6] + '.' + h[0][:4], fontsize=20)
								else:
									jack_date = '%m.%Y'
									plt.title("USD/RUB", fontsize=20)
								ax.xaxis.set_major_formatter(
									matplotlib.dates.DateFormatter(jack_date))  # формат оси x - годы.
								plt.grid()  # наносим сетку.

								plt.savefig(PATH1 + str(event.user_id) + '.png', dpi=1200, format='png', bbox_inches='tight')

								photo1 = add_photo_from_computer(PATH1 + str(event.user_id) + '.png')

								keyboard = get_main_menu_keyboard()
								vk.messages.send(user_id=event.user_id,message='График доллара с ' + data1 + ' по ' + data2 + ':', random_id=get_random_id(), keyboard=keyboard.get_keyboard(), attachment=photo1)
								idslov[event.user_id] = 'menu'
								os.remove(PATH1 + str(event.user_id) + '.png')
							except Exception as E:
								traceback.print_exc()
								print(E)
								keyboard = get_main_menu_keyboard()
								vk.messages.send(user_id=event.user_id, message='Ошибка', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
								idslov[event.user_id] = 'menu'
						else:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Сегодня', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Неправильная запись даты. Повторяю: день.месяц.год', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				# Пароль
				elif idslov[event.user_id] == 'password':
					keyboard = get_main_menu_keyboard()
					if out_game(vksms):
						vk.messages.send(user_id=event.user_id, message='Генератор пароля закрыт✅', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						try:
							num = int(event.text)
							vk.messages.send(user_id=event.user_id, message=password(num), random_id=get_random_id(), keyboard=keyboard.get_keyboard())
							idslov[event.user_id] = 'menu'
						except:
							traceback.print_exc()
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Введите целочисленное число', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				# Калькулятор валют
					# С какой валюты
				elif idslov[event.user_id] == 'calc':
					if out_game(vksms):
						keyboard = get_main_menu_keyboard()
						vk.messages.send(user_id=event.user_id, message='Калькулятор валют закрыт✅',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('🇷🇺', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('🇺🇸', color=VkKeyboardColor.SECONDARY)
						keyboard.add_line()
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						if vksms.count('евро') > 0 or vksms.count('eur') > 0 or vksms.count('🇪🇺') > 0:
							idslov[event.user_id] = 'calc eur'
							vk.messages.send(user_id=event.user_id, message='Введите валюту, на которую хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('франк') > 0 or vksms.count('chf') > 0 or vksms.count('🇨🇭') > 0:
							idslov[event.user_id] = 'calc chf'
							vk.messages.send(user_id=event.user_id, message='Введите валюту, на которую хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('фунт') > 0 or vksms.count('стерлинг') > 0 or vksms.count('gbp') > 0 or vksms.count('🇬🇧') > 0:
							idslov[event.user_id] = 'calc gbp'
							vk.messages.send(user_id=event.user_id, message='Введите валюту, на которую хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('иена') > 0 or vksms.count('иены') > 0 or vksms.count('jpy') > 0 or vksms.count('🇯🇵') > 0:
							idslov[event.user_id] = 'calc jpy'
							vk.messages.send(user_id=event.user_id, message='Введите валюту, на которую хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('казахст') > 0 or vksms.count('тенге') > 0 or vksms.count('kzt') > 0 or vksms.count('🇰🇿') > 0:
							idslov[event.user_id] = 'calc kzt'
							vk.messages.send(user_id=event.user_id, message='Введите валюту, на которую хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif (vksms.count('белорус') > 0 and vksms.count('рубл') > 0) or vksms.count('белорус') > 0 or vksms.count('byn') > 0 or vksms.count('🇧🇾') > 0:
							idslov[event.user_id] = 'calc byn'
							vk.messages.send(user_id=event.user_id, message='Введите валюту, на которую хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('турец') > 0 or vksms.count('лиры') > 0 or vksms.count('лира') > 0 or vksms.count('try') > 0 or vksms.count('🇹🇷') > 0:
							idslov[event.user_id] = 'calc try'
							vk.messages.send(user_id=event.user_id, message='Введите валюту, на которую хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('китай') > 0 or vksms.count('юань') > 0 or vksms.count('юаня') > 0 or vksms.count('cny') > 0 or vksms.count('🇨🇳') > 0:
							idslov[event.user_id] = 'calc cny'
							vk.messages.send(user_id=event.user_id, message='Введите валюту, на которую хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif (vksms.count('австрал') > 0 and vksms.count('доллар') > 0) or vksms.count('австрал') > 0 or vksms.count('aud') > 0 or vksms.count('🇦🇺') > 0:
							idslov[event.user_id] = 'calc aud'
							vk.messages.send(user_id=event.user_id, message='Введите валюту, на которую хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif (vksms.count('канад') > 0 and vksms.count('доллар') > 0) or vksms.count('канад') > 0 or vksms.count('cad') > 0 or vksms.count('🇨🇦') > 0:
							idslov[event.user_id] = 'calc cad'
							vk.messages.send(user_id=event.user_id, message='Введите валюту, на которую хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('польш') > 0 or vksms.count('польск') > 0 or vksms.count('злотый') > 0 or vksms.count('pln') > 0 or vksms.count('🇵🇱') > 0:
							idslov[event.user_id] = 'calc pln'
							vk.messages.send(user_id=event.user_id, message='Введите валюту, на которую хотите перевести:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('корей') > 0 or vksms.count('корея') > 0 or vksms.count('вон') > 0 or vksms.count('krw') > 0 or vksms.count('🇰🇷') > 0:
							idslov[event.user_id] = 'calc krw'
							vk.messages.send(user_id=event.user_id,
								message='Введите валюту, на которую хотите перевести:', random_id=get_random_id(),
								keyboard=keyboard.get_keyboard())
						elif vksms.count('рубл') > 0 or vksms.count('rub') > 0 or vksms.count('🇷🇺') > 0:
							idslov[event.user_id] = 'calc rub'
							vk.messages.send(user_id=event.user_id,
								message='Введите валюту, на которую хотите перевести:', random_id=get_random_id(),
								keyboard=keyboard.get_keyboard())
						elif vksms.count('доллар') > 0 or vksms.count('usd') > 0 or vksms.count('🇺🇸') > 0:
							idslov[event.user_id] = 'calc usd'
							vk.messages.send(user_id=event.user_id,
								message='Введите валюту, на которую хотите перевести:', random_id=get_random_id(),
								keyboard=keyboard.get_keyboard())
						else:
							vk.messages.send(user_id=event.user_id, message='Извините, такой валюты я не знаю, попробуйте еще раз',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())

					# На какую валюту
				elif idslov[event.user_id][:4] == 'calc' and len(idslov[event.user_id]) == 8:
					if out_game(vksms):
						keyboard = get_main_menu_keyboard()
						vk.messages.send(user_id=event.user_id, message='Калькулятор валют закрыт✅',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						if vksms.count('евро') > 0 or vksms.count('eur') > 0 or vksms.count('🇪🇺') > 0:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							idslov[event.user_id] = str(idslov[event.user_id]) + '-eur'
							vk.messages.send(user_id=event.user_id,
								message='Введите количество:', random_id=get_random_id(),
								keyboard=keyboard.get_keyboard())
						elif vksms.count('франк') > 0 or vksms.count('chf') > 0 or vksms.count('🇨🇭') > 0:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							idslov[event.user_id] = str(idslov[event.user_id]) + '-chf'
							vk.messages.send(user_id=event.user_id,
								message='Введите количество:', random_id=get_random_id(),
								keyboard=keyboard.get_keyboard())
						elif vksms.count('фунт') > 0 or vksms.count('стерлинг') > 0 or vksms.count('gbp') > 0 or vksms.count('🇬🇧') > 0:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							idslov[event.user_id] = str(idslov[event.user_id]) + '-gbp'
							vk.messages.send(user_id=event.user_id,
								message='Введите количество:', random_id=get_random_id(),
								keyboard=keyboard.get_keyboard())
						elif vksms.count('иена') > 0 or vksms.count('иены') > 0 or vksms.count('jpy') > 0 or vksms.count('🇯🇵') > 0:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							idslov[event.user_id] = str(idslov[event.user_id]) + '-jpy'
							vk.messages.send(user_id=event.user_id,
								message='Введите количество:', random_id=get_random_id(),
								keyboard=keyboard.get_keyboard())
						elif vksms.count('казахст') > 0 or vksms.count('тенге') > 0 or vksms.count('kzt') > 0 or vksms.count('🇰🇿') > 0:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							idslov[event.user_id] = str(idslov[event.user_id]) + '-kzt'
							vk.messages.send(user_id=event.user_id,
								message='Введите количество:', random_id=get_random_id(),
								keyboard=keyboard.get_keyboard())
						elif (vksms.count('белорус') > 0 and vksms.count('рубл') > 0) or vksms.count('белорус') > 0 or vksms.count('byn') > 0 or vksms.count('🇧🇾') > 0:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							idslov[event.user_id] = str(idslov[event.user_id]) + '-byn'
							vk.messages.send(user_id=event.user_id,
								message='Введите количество:', random_id=get_random_id(),
								keyboard=keyboard.get_keyboard())
						elif vksms.count('турец') > 0 or vksms.count('лиры') > 0 or vksms.count('лира') > 0 or vksms.count('try') > 0 or vksms.count('🇹🇷') > 0:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							idslov[event.user_id] = str(idslov[event.user_id]) + '-try'
							vk.messages.send(user_id=event.user_id,
								message='Введите количество:', random_id=get_random_id(),
								keyboard=keyboard.get_keyboard())
						elif vksms.count('китай') > 0 or vksms.count('юань') > 0 or vksms.count('юаня') > 0 or vksms.count('cny') > 0 or vksms.count('🇨🇳') > 0:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							idslov[event.user_id] = str(idslov[event.user_id]) + '-cny'
							vk.messages.send(user_id=event.user_id,
								message='Введите количество:', random_id=get_random_id(),
								keyboard=keyboard.get_keyboard())
						elif (vksms.count('австрал') > 0 and vksms.count('доллар') > 0) or vksms.count('австрал') > 0 or vksms.count('aud') > 0 or vksms.count('🇦🇺') > 0:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							idslov[event.user_id] = str(idslov[event.user_id]) + '-aud'
							vk.messages.send(user_id=event.user_id,
								message='Введите количество:', random_id=get_random_id(),
								keyboard=keyboard.get_keyboard())
						elif (vksms.count('канад') > 0 and vksms.count('доллар') > 0) or vksms.count('канад') > 0 or vksms.count('cad') > 0 or vksms.count('🇨🇦') > 0:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							idslov[event.user_id] = str(idslov[event.user_id]) + '-cad'
							vk.messages.send(user_id=event.user_id,
								message='Введите количество:', random_id=get_random_id(),
								keyboard=keyboard.get_keyboard())
						elif vksms.count('польш') > 0 or vksms.count('польск') > 0 or vksms.count('злотый') > 0 or vksms.count('pln') > 0 or vksms.count('🇵🇱') > 0:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							idslov[event.user_id] = str(idslov[event.user_id]) + '-pln'
							vk.messages.send(user_id=event.user_id,
								message='Введите количество:', random_id=get_random_id(),
								keyboard=keyboard.get_keyboard())
						elif vksms.count('корей') > 0 or vksms.count('корея') > 0 or vksms.count('вон') > 0 or vksms.count('krw') > 0 or vksms.count('🇰🇷') > 0:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							idslov[event.user_id] = str(idslov[event.user_id]) + '-krw'
							vk.messages.send(user_id=event.user_id,
								message='Введите количество:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('рубл') > 0 or vksms.count('rub') > 0 or vksms.count('🇷🇺') > 0:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							idslov[event.user_id] = str(idslov[event.user_id]) + '-rub'
							vk.messages.send(user_id=event.user_id,
								message='Введите количество:', random_id=get_random_id(),
								keyboard=keyboard.get_keyboard())
						elif vksms.count('доллар') > 0 or vksms.count('usd') > 0 or vksms.count('🇺🇸') > 0:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							idslov[event.user_id] = str(idslov[event.user_id]) + '-usd'
							vk.messages.send(user_id=event.user_id,
								message='Введите количество:', random_id=get_random_id(),
								keyboard=keyboard.get_keyboard())
						else:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('🇷🇺', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('🇺🇸', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id,
								message='Извините, такой валюты я не знаю, попробуйте еще раз',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())

					# Количество
				elif idslov[event.user_id][:4] == 'calc' and len(idslov[event.user_id]) == 12:
					keyboard = get_main_menu_keyboard()
					if vksms == 'выйти' or vksms == 'отмена':
						vk.messages.send(user_id=event.user_id, message='Калькулятор валют закрыт✅',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						try:
							x = float(event.text)
							Values = calculator_of_currencies(idslov[event.user_id][5:] + '_' + event.text)
							vk.messages.send(user_id=event.user_id, message=Values, random_id=get_random_id(),
								keyboard=keyboard.get_keyboard())
							idslov[event.user_id] = 'menu'
						except:
							traceback.print_exc()
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Введи ПРОСТО ЧИСЛО',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				# Яндекс Переводчик
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
				# Морзе
				elif idslov[event.user_id] == 'morz':
					if vksms == 'выйти' or vksms == 'отмена':
						keyboard = get_main_menu_keyboard()
						vk.messages.send(user_id=event.user_id, message='Переводчик Морзе закрыт✅',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						if event.text == '1':
							idslov[event.user_id] = 'morz1'
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('+', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id,
							message='Введите сообщение, которое вы хотите записать из русского на Азбуку Морзе или введите "+", ' \
							'чтобы посмотреть всю Азбуку Морзе:\n(вы можете использовать прописные и строчные буквы русского языка, знаки препинания, цифры)',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif event.text == '2':
							idslov[event.user_id] = 'morz2'
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('+', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id,
							message='Введите КОЛИЧЕСТВО СЛОВ в вашем сообщении или введите "+", чтобы посмотреть всю Азбуку Морзе:',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						else:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('1', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('2', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('3', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('4', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Отправь "1", "2", "3" или "4"',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())

				elif idslov[event.user_id] == 'morz1':
					if event.text == 'Отмена':
						keyboard = get_main_menu_keyboard()
						vk.messages.send(user_id=event.user_id,
						message='Переводчик Морзе закрыт✅\n(если ты хотел перевести в морзе "ОТМЕНА", напиши с маленькой буквы)',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						if event.text == '+':
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('+', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id,
							message='АЗБУКА МОРЗЕ:\nА *—\nБ —***\nВ *——\nГ ——*\nД —**\nЕ и Ё *\nЖ ***—\nЗ ——**\nИ **\nЙ *———\nК —*—\nЛ *—**\nМ ——\nН —*\nО ———\nП *——*\nР *—*\nС ***\nТ —\nУ **—\nФ **—*\nХ ****\nЦ —*—*\nЧ ———*\nШ ————\nЩ ——*—\nЪ *——*—\nЫ —*——\nЬ —**—\nЭ **—**\nЮ **——\nЯ *—*—\n0 —————\n1 *————\n2 **———\n3 ***——\n4 ****—\n5 *****\n6 —****\n7 ——***\n8 ———**\n9 ————*\n. ******\n, *—*—*—\n: ———***\n; —*—*—*\n( и ) —*——*—\n? **——**\n! ——**——\n" и ' + "'" + ' *—**—*',
							random_id=get_random_id())
							vk.messages.send(user_id=event.user_id,
							message='Введите сообщение, которое вы хотите записать из русского на Азбуку Морзе или введите "+", ' \
							'чтобы посмотреть всю Азбуку Морзе:\n(вы можете использовать прописные и строчные буквы русского языка, знаки препинания, цифры)',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						else:
							idslov[event.user_id] = 'menu'
							v_morze1 = v_morze(event.text)
							keyboard = get_main_menu_keyboard()
							if v_morze1.count('/') > 0:
								keyboard.add_button('Что за палки /?', color=VkKeyboardColor.SECONDARY)
								keyboard.add_line()

							vk.messages.send(user_id=event.user_id, message=v_morze1, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
							if v_morze1.count('_') > 0 and v_morze1.count('.') > 0:
								v_morze2 = v_morze1.replace('_', '—')
								v_morze2 = v_morze2.replace('.', '*')
								vk.messages.send(user_id=event.user_id, message=v_morze2, random_id=get_random_id())
				elif idslov[event.user_id] == 'morz2':
					if out_game(vksms):
						keyboard = get_main_menu_keyboard()
						vk.messages.send(user_id=event.user_id, message='Переводчик Морзе закрыт✅', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						if event.text == '+':
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('+', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id,
							message='АЗБУКА МОРЗЕ:\nА *—\nБ —***\nВ *——\nГ ——*\nД —**\nЕ и Ё *\nЖ ***—\nЗ ——**\nИ **\nЙ *———\nК —*—\nЛ *—**\nМ ——\nН —*\nО ———\nП *——*\nР *—*\nС ***\nТ —\nУ **—\nФ **—*\nХ ****\nЦ —*—*\nЧ ———*\nШ ————\nЩ ——*—\nЪ *——*—\nЫ —*——\nЬ —**—\nЭ **—**\nЮ **——\nЯ *—*—\n0 —————\n1 *————\n2 **———\n3 ***——\n4 ****—\n5 *****\n6 —****\n7 ——***\n8 ———**\n9 ————*\n. ******\n, *—*—*—\n: ———***\n; —*—*—*\n( и ) —*——*—\n? **——**\n! ——**——\n" и ' + "'" + ' *—**—*',
							random_id=get_random_id())
							vk.messages.send(user_id=event.user_id,
							message='Введите КОЛИЧЕСТВО СЛОВ в вашем сообщении или введите "+", чтобы посмотреть всю Азбуку Морзе:',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						else:
							try:
								sms = int(event.text)
								idslov[event.user_id] = 'morz2.1/' + str(sms)
								morslov[event.user_id] = ''
								keyboard = VkKeyboard(one_time=True)
								keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
								vk.messages.send(user_id=event.user_id, message='Введите 1 слово:', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
							except:
								traceback.print_exc()
								keyboard = VkKeyboard(one_time=True)
								keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
								vk.messages.send(user_id=event.user_id, message='Просто введи число', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				elif str(idslov[event.user_id])[:6] == 'morz2.':
					if out_game(vksms):
						keyboard = get_main_menu_keyboard()
						vk.messages.send(user_id=event.user_id, message='Переводчик Морзе закрыт✅', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						a = idslov[event.user_id].find('/')
						int_from = int(str(idslov[event.user_id])[6:a])
						int_to = int(str(idslov[event.user_id])[a + 1:])
						if int_from < int_to:
							sms = iz_morze(event.text)
							if sms == 'Ошибка':
								sms = 'ОШИБКА'
							if int_from == 1:
								morslov[event.user_id] += sms
							else:
								morslov[event.user_id] += ' ' + sms
							int_from += 1
							idslov[event.user_id] = 'morz2.' + str(int_from) + '/' + str(int_to)
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Введите ' + str(int_from) + ' слово:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						else:
							sms = iz_morze(event.text)
							if sms == 'Ошибка':
								sms = 'ОШИБКА'
							if int_from == 1:
								morslov[event.user_id] += sms
							else:
								morslov[event.user_id] += ' ' + sms
							keyboard = get_main_menu_keyboard()
							vk.messages.send(user_id=event.user_id, message=morslov[event.user_id],
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())

							morslov[event.user_id] = '0'
							idslov[event.user_id] = 'menu'
	except Exception as E:
		print('Ошибка: ' + str(E))
		traceback.print_exc()
		print('Перезапуск...')
		time.sleep(1)