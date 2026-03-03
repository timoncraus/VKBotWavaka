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

# Получение данных о id пользователей
print('Запускаем бота на:')
print('1 - На компьютере')
print('2 - На сервере (по умолчанию)')
print('3 - Указать путь к файлам самостоятельно')
fhg = str(input('>>>'))
if fhg == '1':
	file = 'idlist.txt'
	file2 = 'stab.txt'
	uuu = 1
	uum = -2
elif fhg == '3':
	file = str(input('Введите путь к файлу с id пользователей:'))
	file2 = str(input('Введите путь к файлу с количеством сообщением:'))
	uuu = 0
	uum = 0
else:
	file = '/home/ttimoncraus/idlist - vk_bot.txt'
	file2 = '/home/ttimoncraus/stab.txt'
	uuu = -3
	uum = -1

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
token1 = '!СЕКРЕТНЫЙ ТОКЕН!'
group_id = '!НОМЕР ГРУППЫ!'
vk_session = vk_api.VkApi(token=token1)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
# Некоторые переменные:
sub = ''
version = '2.3'
str_games = 'Чтобы выбрать игру, напиши соответствующую цифру:' \
			'\n1) Орел и решка' \
			'\n2) Отгадай число' \
			'\n3) Быки и коровы' \
			'\n4) Виселица'
str_skills = 'Вот, что я умею:' \
			 '\n🎦 Напиши "что посмотреть" или "что глянуть" и т.д., чтобы войти в меню просмотра нашей подборки лучших сериалов и фильмов' \
			 '\n⭐ Напиши "википедия", "вики", "wikipedia", "wiki" и т.д., чтобы найти что-либо в Википедии' \
			 '\n⭐ Напиши "переводчик", "перевод", "переведи", "перевести" и т.д., чтобы перевести текст с одного языка на другой' \
			 '\n⭐ Напиши "переводчик морзе", "перевод морзе", "морзе", "морзянка" и т.д., чтобы перевести текст в морзянку и обратно' \
			 '\n⭐ Напиши "скажи погоду", "узнать погоду", "погода" и т.д., чтобы узнать погоду в том или ином городе/стране' \
			 '\n⭐ Напиши "игры", "играть", "давай поиграем", "поигрунькать", и т.д., чтобы открыть список игр' \
			 '\n⭐ Напиши "факты", "интересный факт", "расскажи факт" и т.д., чтобы узнать случайный факт'\
			 '\n⭐ Напиши "время", "день недели", "сезон" и т.д., чтобы узнать в каком временном отрезке ты сейчас находишься'\
			 '\n⭐ Напиши "сколько дней в сентябре", "сколько дней в марте" и т.д., чтобы узнать количество дней в том или ином месяце' \
			 '\n⭐ Напиши "курс доллара", "курс евро" и т.д., чтобы узнать курс той или иной валюты к рублю (чтобы узнать, какие валюты доступны, напиши "валюты")'\
			 '\n⭐ Напиши "калькулятор валют", чтобы перевести количество одной валюты в другую'\
			 '\n⭐ Напиши "ландыши", "розы", "ромашка" и т.д., чтобы получить фото тех или иных цветов (чтобы узнать, какие цветы доступны, напиши "цветы")' \
			 '\n⭐ Напиши "глитч" или "glitch", чтобы получить случайный набор символов' \
			 '\n⭐ Напиши "глитч слова" или "glitch слово" и т.д., чтобы зашифровать свое сообщение случайным набором символов' \
			 '\n⭐ Напиши "стабильность", чтобы узнать, сколько бот отправил сообщений, начиная с 27.03.20' \
             '\n🔆 А вообще можешь просто со мной поболтать😄'
str_data_v = 'Версия ' + version + '\nДаты других версий: ' \
								   '\n"test_group", "bot_tima" - 1.0 (17.02.2020)' \
								   '\n"Wavaka" - 2.0 (23.02.20)' \
								   '\n"Wavaka" - 2.1 (8.03.20)' \
								   '\n"Wavaka" - 2.2 (27.03.20)' \
								   '\n"Wavaka" - 2.3 (22.04.20)'
str_flowers = '🌺Вот, какие цветы доступны:' \
			  '\nРозы, гвоздики, тюльпаны, ромашки, ландыши, подсолнух, нарциссы, мимозы, герберы, орхидеи, ирисы, сирени, гардении, жасмины, магнолии, гиацинты, гладиолусы'
str_value = 'Вот все доступные мне валюты:' \
			'\n🇷🇺Рубль (RUB)' \
			'\n🇺🇸Доллар США (USD)' \
			'\n🇪🇺Евро (EUR)' \
			'\n🇨🇭Швейцарский франк (CHF)' \
			'\n🇬🇧Фунт стерлингов (GBP)' \
			'\n🇯🇵Иена (JPY)' \
			'\n🇺🇦Украинская гривна (UAH)' \
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
	facts = ['1525000000 км телефонного провода натянуто по всей территории США.', '111111111х111111111 = 123456789',
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

def rope_word(): # Слова для игры "Виселица"
	words = ['стакан', 'сахар', 'кефир', 'кофе', 'кофеварка', 'резина', 'солдат', 'офицер', 'таблетка', 'прошлое', 'письмо', 'поэма',
			 'сочинение', 'подставка', 'чугун', 'перо', 'продолжение', 'телефон', 'будка', 'облако', 'термометр', 'шрифт', 'стройка',
			 'носорог', 'юла', 'свет', 'лампа', 'ветка', 'дерево', 'улыбка', 'настроение', 'конфета', 'овца', 'фантик', 'комикс', 'фамилия',
			 'тапок', 'тряпка', 'мяч', 'меч', 'муж', 'кошка', 'кот', 'конь', 'кочка', 'канава', 'путь', 'карета', 'ось', 'косарь', 'комар',
			 'шёпот', 'шомпол', 'мороз', 'вата', 'пластырь', 'небо', 'антисептик', 'гонг', 'гной', 'рана', 'шов', 'йод', 'перечень', 'кровь',
			 'лимфа', 'сердце', 'мозг', 'пузырь', 'моча', 'желудок', 'плоть', 'жало', 'яд', 'смерть', 'предательство', 'плотность',
			 'население', 'кинжал', 'сабля', 'нагайка', 'кунжут', 'кнут', 'орех', 'миндаль', 'казинка', 'халва', 'шоколад', 'какао',
			 'молоко', 'мёд', 'патока', 'виноград', 'груша', 'семя', 'глаз', 'нос', 'рот', 'род', 'щит', 'рапира', 'шпатель', 'телеграф',
			 'любовник', 'жена', 'бастард', 'полет', 'мышь', 'птица', 'самолёт', 'поле', 'казак', 'казан', 'мангал', 'бар', 'водка',
			 'вода', 'ром', 'марш', 'пират', 'корсар', 'постель', 'король', 'корона', 'уборка', 'изумруд', 'рубин', 'яшма', 'артерия',
			 'вена', 'парад', 'сезон', 'авиация', 'быль', 'герой', 'сказка', 'богатырь', 'арбуз', 'ягода', 'кобыла', 'колбаса', 'кабачок',
			 'яйцо', 'стул', 'электричество', 'шёлк', 'шляпа', 'металл', 'кепка', 'выключатель', 'сеть', 'червь', 'анализ', 'вирус', 'память',
			 'народ', 'эпос', 'этнос', 'ковёр', 'карантин', 'сумма', 'право', 'суд', 'кресло', 'профилактика', 'соль', 'вагон', 'лапша',
			 'земля', 'воздух', 'печенье', 'пирожное', 'жалость', 'топор', 'рыба', 'дельфин', 'кристалл', 'бриллиант', 'холм', 'гора', 'уступ',
			 'негр', 'репа', 'свекла', 'рожь', 'доля', 'лапа', 'фура', 'ферма', 'лодка', 'катер', 'чай', 'цвет', 'цветок', 'сугроб', 'щавель',
			 'цыган', 'цыпа', 'цыпочки', 'перила', 'метро', 'фартук', 'кегля', 'знамя', 'барабан', 'палка', 'жердь', 'ботинок', 'элеватор',
			 'дятел', 'насморк', 'яблоко', 'яхта', 'крейсер', 'якорь', 'людоед', 'жертва', 'посёлок', 'деревня', 'буква', 'город', 'дом', 'район',
			 'квартал', 'улица', 'квартира', 'стол', 'ручка', 'учебник', 'страница', 'строка', 'абзац', 'пенал', 'лупа', 'шар', 'рак', 'циркуль',
			 'цирк', 'калькулятор', 'химия', 'физика', 'скаут', 'пионер', 'автомат', 'форма', 'узел', 'винтовка', 'пистолет', 'пушка', 'патрон',
			 'ноготь', 'палец', 'дыра', 'гильза', 'пояс', 'куш', 'верность', 'вера', 'викторина', 'вентиль', 'вензель', 'выкрутас', 'вектор',
			 'вече', 'вечеринка', 'волос', 'вой', 'волк', 'вол', 'вопль', 'ворот', 'вор', 'век', 'вьюга', 'вялость', 'пельмень', 'перец', 'варка',
			 'песок', 'пятка', 'пинцет', 'река', 'насос', 'пень', 'грязь', 'хурма', 'жёлудь', 'дождь', 'снег', 'град', 'ураган', 'засуха', 'ветер',
			 'цунами', 'землетрясение', 'торнадо', 'солнцепёк', 'вихрь', 'цепь', 'нож', 'сечь', 'пожар', 'огонь', 'лёд', 'дедушка', 'шапка', 'хохол',
			 'гайка', 'робот', 'сын', 'царь', 'шишка', 'день', 'ночь', 'рать', 'жаба', 'полдень', 'винт', 'фара', 'зонт', 'нога', 'шпага']
	return random.choice(words)
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
	elif fr == 'UAH':
		if c == float(c):
			if (c >= 5 and c <= 20) or (c % 10 == 0 or c % 10 >= 5):
				return 'украинских гривен 🇺🇦'
			elif (c >= 2 and c <= 4) or (c % 10 >= 2 and c % 10 <= 4):
				return 'украинских гривны 🇺🇦'
			elif c == 1 or c % 10 >= 1 and c > 10:
				return 'украинская гривна 🇺🇦'
			else:
				return 'украинских гривен 🇺🇦'
		else:
			return 'украинских гривны 🇺🇦'
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
					keyboard = VkKeyboard(one_time=True)
					keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
					keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
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
						 '\n🎦 (при поддержке [id356556313|Борискина Николая]) Обновление функции "Что посмотреть" в честь карантина - добавлено аниме'
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
						vk.messages.send(user_id=event.user_id, message='Сейчас по Московскому времени ' + str(now.hour-uuu) + ':' + tt_m + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
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
					elif (vksms.count('слава') > 0) and (vksms.count('украине') > 0 or vksms.count('украiне') > 0 or vksms.count('україне') > 0):
						vk.messages.send(user_id=event.user_id, message='Героям слава🇺🇦' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('украин') > 0 or vksms.count('украiн') > 0 or vksms.count('україн') > 0:
						vk.messages.send(user_id=event.user_id, message='Слава Украине🇺🇦' + sub, random_id=get_random_id(),
							keyboard=keyboard.get_keyboard())
					elif vksms.count('героям') > 0 or vksms.count('слава') > 0:
						vk.messages.send(user_id=event.user_id, message='Это точно🇺🇦' + sub,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('ссср') > 0 or (vksms.count('советский') > 0 and vksms.count('союз') > 0) or (
						vksms.count('союз') > 0 and vksms.count('советских') > 0 and vksms.count('социал') > 0 and vksms.count('республ') > 0):
						photo = add_photo('https://avatars.mds.yandex.net/get-pdb/2497678/e39922f0-7615-4503-bd37-0e0a42f7469e/s1200')
						vk.messages.send(user_id=event.user_id, message='Слава Советскому Союзу!' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard(), attachment=photo)
					elif vksms.count('казахстан') > 0 or vksms.count('казакстан') > 0:
						photo = add_photo('https://avatars.mds.yandex.net/get-pdb/1348397/04aee01d-10f5-4048-b845-fd8787c0a836/s1200?webp=false')
						vk.messages.send(user_id=event.user_id, message='Казахстан - страна будущего' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
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
					)) or vksms.count('умения') > 0 or vksms.count('способности') > 0:
						keyboard.add_line()
						keyboard.add_button('P.S.', color=VkKeyboardColor.SECONDARY)
						vk.messages.send(user_id=event.user_id, message=str_skills + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('аллах') > 0:
						vk.messages.send(user_id=event.user_id, message='Аллах над нами,\nЗемля под нами,\nНож в кармане,\nВперёд, мусульмане!' + sub,
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif (vksms.count('бля') > 0 or vksms.count('сук') > 0 or vksms.count(
						'еб') > 0 or vksms.count('ёб') > 0 or vksms.count(
						'сучка') > 0 or vksms.count('шлюх') > 0 or vksms.count(
						'пизд') > 0 or vksms.count('дерьм') > 0 or vksms.count(
						'говн') > 0 or vksms.count('хрен') > 0 or vksms.count(
						'пезд') > 0 or vksms.count('пёзд') > 0 or vksms.count(
						'мудак') > 0 or vksms.count('хуя') > 0 or vksms.count(
						'курва') > 0 or vksms.count(
						'муфлон') > 0 or vksms.count('хуя') > 0 or vksms.count(
						'жоп') > 0 or vksms.count('хуй') > 0 or vksms.count(
						'хуе') > 0) and not(vksms.count('теб') > 0) and not(
						vksms.count('блямба') > 0) and not(vksms.count(
						'сабл') > 0) and vksms!=('сук') and not (vksms.count(
						'бляшка') > 0) and not(vksms.count('сукно') > 0) and not(vksms.count('рубля') > 0):
						vk.messages.send(user_id=event.user_id, message='Без мата пожалуйста😡' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					# Вызов глитч слово
					elif (vksms.count('слов') > 0 or vksms.count('word') > 0) and (vksms.count('глитч') > 0 or vksms.count('glitch') > 0):
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Введите сообщение:', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'glitch_word'
					# Вызов глитч
					elif vksms.count('глитч') > 0 or vksms.count('glitch') > 0:
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Введите количество символов:',random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'glitch'
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
						elif vksms.count('украин') > 0 or vksms.count('гривн') > 0 or vksms.count('uah') > 0 or vksms.count('🇺🇦') > 0:
							UAH10 = str(rates['UAH'].value)[:5]
							c = int(float(UAH10))
							if c == float(UAH10):
								UAH10 = str(int(UAH10))
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
							vk.messages.send(user_id=event.user_id, message='🇺🇦Курс украинской гривны:\n10 гривен = ' + UAH10 + paste + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
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
										 '\n🇺🇦Курс украинской гривны:\n10 гривен = ' + UAH10 + ' рубля' \
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
					# Вызов цветов
					elif vksms.count('цветы') > 0 or vksms.count('цветочки') > 0:
						vk.messages.send(user_id=event.user_id, message=str_flowers + sub,
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('ландыш') > 0:
						photo = add_photo('https://sun9-61.userapi.com/c205528/v205528348/9d6ae/b00Z09oFkuE.jpg')
						vk.messages.send(user_id=event.user_id, message='Вот тебе ландыши:' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('роз') > 0:
						photo = add_photo('https://sun9-29.userapi.com/c206616/v206616348/9cceb/4jaLGXezVOM.jpg')
						vk.messages.send(user_id=event.user_id, message='Вот тебе розы:' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('гвоздик') > 0:
						photo = add_photo('https://sun9-68.userapi.com/c857528/v857528348/19d8b2/WbqEkRR1HCg.jpg')
						vk.messages.send(user_id=event.user_id, message='Вот тебе гвоздики:' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('тюльпан') > 0:
						photo = add_photo('https://sun9-63.userapi.com/c858120/v858120348/1a19c9/D4oKonhbbDs.jpg')
						vk.messages.send(user_id=event.user_id, message='Вот тебе тюльпаны:' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('ромашк') > 0:
						photo = add_photo('https://sun9-59.userapi.com/c853528/v853528348/201b22/itsle2WrDRA.jpg')
						vk.messages.send(user_id=event.user_id, message='Вот тебе ромашки:' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('подсолнух') > 0:
						photo = add_photo('https://sun9-50.userapi.com/c857632/v857632348/19ef38/_8Aukj5q1Tk.jpg')
						vk.messages.send(user_id=event.user_id, message='Вот тебе подсолнухи:' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('нарцисс') > 0:
						photo = add_photo('https://sun9-4.userapi.com/c857536/v857536348/19dab0/Z6iouCRkib0.jpg')
						vk.messages.send(user_id=event.user_id, message='Вот тебе нарциссы:' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('гербер') > 0:
						photo = add_photo('https://sun9-9.userapi.com/c205224/v205224348/9c5da/4YpVGDrXZO4.jpg')
						vk.messages.send(user_id=event.user_id, message='Вот тебе герберы:' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('орхиде') > 0:
						photo = add_photo('https://sun9-11.userapi.com/c857416/v857416348/1a0529/JyNd9fx-VGs.jpg')
						vk.messages.send(user_id=event.user_id, message='Вот тебе орхидеи:' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('ирис') > 0:
						photo = add_photo('https://sun9-11.userapi.com/c206620/v206620348/9bede/5Qi4ezrwBhU.jpg')
						vk.messages.send(user_id=event.user_id, message='Вот тебе ирисы:' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('сирень') > 0 or vksms.count('сирени') > 0:
						photo = add_photo('https://sun9-49.userapi.com/c206528/v206528348/9af98/u_8P-jDAoGg.jpg')
						vk.messages.send(user_id=event.user_id, message='Вот тебе сирени:' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('гардени') > 0:
						photo = add_photo('https://sun9-55.userapi.com/c858432/v858432348/199dd9/leScnCrxnjA.jpg')
						vk.messages.send(user_id=event.user_id, message='Вот тебе гардении:' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('жасмин') > 0:
						photo = add_photo('https://sun9-15.userapi.com/c205824/v205824348/9e489/DX-OQD0mgK4.jpg')
						vk.messages.send(user_id=event.user_id, message='Вот тебе жасмины:' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('магноли') > 0:
						photo = add_photo('https://sun9-21.userapi.com/c858436/v858436348/19a353/id2wzRs8778.jpg')
						vk.messages.send(user_id=event.user_id, message='Вот тебе магнолии:' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('гиацинт') > 0:
						photo = add_photo('https://sun9-4.userapi.com/c857520/v857520348/19d537/g3m59HOPhd8.jpg')
						vk.messages.send(user_id=event.user_id, message='Вот тебе гиацинты:' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('мимоз') > 0:
						photo = add_photo('https://sun9-18.userapi.com/c854324/v854324348/2073ba/VMf9qyi43kI.jpg')
						vk.messages.send(user_id=event.user_id, message='Вот тебе мимозы:' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('гладиолус') > 0:
						photo = add_photo('https://sun9-4.userapi.com/c206828/v206828425/9b33d/UffZ8q1XiWI.jpg')
						vk.messages.send(user_id=event.user_id, message='Вот тебе гладиолусы:' + sub, attachment=photo,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					# Вызов Что Посмотреть
					elif (vksms.count('что') > 0 or vksms.count('че') > 0 or vksms.count('чё') > 0) and (vksms.count('посмотреть') > 0 or vksms.count('глянуть') > 0):
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Сериалы', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Фильмы', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Аниме', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id,
							message='Выберите категорию:',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'l_menu'
					# Вызов Википедии
					elif vksms.count('вики') > 0 or vksms.count('wiki') > 0:
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Введите запрос', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'wiki'
					# Вызов графика доллара
					elif vksms.count('график') > 0:
						if not(file == 'C:\\Users\\Timofey\\Desktop\\idlist - vk_bot.txt'):
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Вы вошли в меню просмотра графика доллара по отношению к рублю', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
							vk.messages.send(user_id=event.user_id, message='Введите дату в формате 25.01.2020, С КОТОРОЙ вы хотите посмотреть график' , random_id=get_random_id(), keyboard=keyboard.get_keyboard())
							idslov[event.user_id] = 'chart'
						else:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
							keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
							vk.messages.send(user_id=event.user_id,message='К сожалению, просмотр графика доллара по отношению к рублю сейчас недоступен((',random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					# Вызов Погоды
					elif vksms.count('погод') > 0:
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='В каком городе/стране вы бы хотели узнать погоду?', random_id=get_random_id(),
							keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'weath'
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
					# Вызов Яндекс Переводчика
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
					# Вызов поиграть
					elif vksms.count('игр') > 0 and vksms.count('тигр') == 0:
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('1', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('2', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('3', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('4', color=VkKeyboardColor.SECONDARY)
						keyboard.add_line()
						keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message=str_games, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'play'
					else:
						vk.messages.send(user_id=event.user_id,
							message='Извини, я не знаю, что такое "' + event.text + '"' + sub, random_id=get_random_id(),
							keyboard=keyboard.get_keyboard())
				# Википедия
				elif idslov[event.user_id] == 'wiki':
					keyboard = VkKeyboard(one_time=True)
					keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
					keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
					if vksms == 'выйти' or vksms == 'отмена':
						vk.messages.send(user_id=event.user_id, message='Википедия закрыта✅', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						try:
							Seacher = 'Вот что я нашёл:\n' + str(wikipedia.summary(event.text)) + sub
						except:
							Seacher = 'Статья не найдена' + sub
						vk.messages.send(user_id=event.user_id, message= Seacher, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
				# Что Посмотреть
				elif idslov[event.user_id] == 'l_menu':
					if out_game(vksms):
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
						vk.messages.send(user_id=event.user_id, message='Функция "Что посмотреть" закрыта✅', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						if vksms == 'сериал' or vksms == 'сериалы':
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Детектив', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фантастика', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Ужасы', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Выберите жанр сериала:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
							idslov[event.user_id] = 'l_series'
						elif vksms == 'фильм' or vksms == 'фильмы':
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Детектив', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фантастика & фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Ужасы', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Выберите жанр фильма:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
							idslov[event.user_id] = 'l_films'
						elif vksms == 'аниме':
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Приключения', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Мафия', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Мистика', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Выберите жанр аниме:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
							idslov[event.user_id] = 'l_anime'
						else:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Сериалы', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фильмы', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Аниме', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Извини, я не знаю такой категории', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				elif idslov[event.user_id] == 'l_series':
					if out_game(vksms):
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Сериалы', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Фильмы', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Аниме', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Выберите категорию:', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'l_menu'
					else:
						if vksms == 'детектив' or vksms == 'детективы':
							vk.messages.send(user_id=event.user_id, message='👀Вот, какие сериалы на жанр "Детектив" у меня есть:' + sub, random_id=get_random_id())
							photo = add_photo('https://sun9-66.userapi.com/c858136/v858136909/1a2d4f/1vcUnvcqM9E.jpg')
							vk.messages.send(user_id=event.user_id, message='《Шерлок Холмс》\nОценка 9/10\n4 сезона\n\nЭтот человек обладает сверхчеловеческим умом и смекалкой. Он может раскусить замысел любого жулика или бандита. Шерлок – является уникумом среди сыщиков, который может распутать любое дело за считанные часы. '
							                                                'Его работа трудна и опасна. В округе ходят слухи о славе гения преступного мира и его талантах. Но уникум не так уж и прост: он умен, хитёр и проворен. Если, кто-то положить глаз на жизнь Шерлока или его имущество, то ему это не удастся. '
							                                                'Шерлок тесно сотрудничает с органами правопорядка и помогает им находить преступников, и обезвреживать их. Если бы не его смекалка и ум, то половина годовых дел полицейского участка не была раскрыта. Благодаря нему, показатель преступности в округе снизился, а общая атмосфера города перешла в нормальное русло. '
							                                                'У следопыта есть друг Ватсон, он помогает ему в расследованиях и додумывает его гениальные идеи. Это его верный друг и помощник, без него Шерлок лишился бы значительной части своих раскрытых дел и удивительных находок',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-21.userapi.com/c854016/v854016909/2119ea/a2MFaMJLB94.jpg')
							vk.messages.send(user_id=event.user_id, message='《Доктор Хаус》\nОценка 9/10\n8 сезонов\n\nДоктор Хаус – это циничный, ироничный и кажущийся иногда совершенно бесчувственным герой одноименного сериала, все серии которого вы можете смотреть онлайн на нашем фан-сайте. Все его выходки сходят с рук, '
							                                                'потому что он гениальный диагност, спасающий жизни, когда другие врачи опускают руки. Если на кону жизнь пациента, Хаус и команда не остановятся даже перед проникновением в дом, офис, машину или личную жизнь больного, и эта нестандартная тактика действует! '
								                                            'Хаус предпочитает лечить своих пациентов, не встречаясь с ними, или ограничив общение к минимуму. Доктор не просто так саркастичен и не любит людей. Борясь за жизни других, он не в состоянии избавить себя самого как от боли физической, что постоянно терзает ногу, делая его жестче и циничнее, '
							                                                'так и от моральных переживаний и одиночества. Боль в ноге делает его характер невыносимым, он кажется бесчеловечным и иногда жестоким, но от этого он не перестает быть гением своего дела. Пациенты-загадки для него, как наркотик. Хоть в излечении он преследует',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-25.userapi.com/c857320/v857320909/125534/JmRmLlBBysU.jpg')
							vk.messages.send(user_id=event.user_id, message='《Настоящий детектив》\nОценка 9/10\n3 сезона\n\nАнтология, в каждом сезоне которой представляются новые персонажи, расследуются различные преступления, происходившие в различные промежутки времени. Помимо, собственно, детективной составляющей, ключевым элементом проекта являются сложные взаимоотношения между главными героями.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-48.userapi.com/c206616/v206616909/b2cde/1EnnqYjG1kY.jpg')
							vk.messages.send(user_id=event.user_id,message='《Твин Пикс》\nОценка 9/10\n1 сезон\n\nИстория начинается с известия о находке обнаженного тела старшеклассницы Лоры Палмер, завёрнутого в полиэтилен и выброшенного волнами на берег озера. В ходе расследования перед внимательными взглядами агента Купера, шерифа Трумана и его помощников проходят разные жители Твин Пикс. '
								                                            'Постепенно зритель открывает для себя темную и страшную сторону жизни обитателей на первый взгляд тихого и мирного городка.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-70.userapi.com/c858236/v858236909/1aea47/zevVUuqVrBo.jpg')
							vk.messages.send(user_id=event.user_id, message='Лютер\nОценка 8/10\n5 сезонов\n\nГоворят,что Лютер создан под влиянием персонажей Шерлока Холмса и Коломбо. Методы раскрытия преступления взяты у Шерлока, а концепция '
								                                            'сериала, в которой убийца зрителю известен, но пока еще не пойман — наследие Коломбо. Так или иначе, стоит отметить, что преступники и их деяния, а также само раскрытие '
								                                            'преступлений, часто отходят на второй план. На плане первом — харизма детектива, его персональные и семейные проблемы, из-за которых он часто сам совершает поступки весьма '
								                                            'спорного характера. Это неудивительно, ведь в главной роли — Идрис Эльба. Четыре коротких сезона, которые однозначно претендуют на право быть просмотренными всеми '
								                                            'любителями детективного жанра.',
								                             		     	attachment=photo, random_id=get_random_id())
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Детектив', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фантастика', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Ужасы', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Выберите жанр сериала:', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms == 'драмма' or vksms == 'драммы':
							vk.messages.send(user_id=event.user_id, message='👀Вот, какие сериалы на жанр "Драмма" у меня есть:' + sub, random_id=get_random_id())
							photo = add_photo('https://sun9-21.userapi.com/c857232/v857232905/121e94/oyQEQwBuDbY.jpg')
							vk.messages.send(user_id=event.user_id, message='《Бесстыжие》\nОценка 9/10\nСезонов 11\n\nАмериканский ремейк британского сериала, повествующий о взбалмошной многодетной семье Галлахеров и их соседях, которые веселятся,попадают '
								                                            'в самые невероятные ситуации и пытаются выжить в этом мире всеми возможными средствами, но при этом как можно меньше работая.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-46.userapi.com/c857016/v857016905/122041/ZgdBB9s2pWo.jpg')
							vk.messages.send(user_id=event.user_id, message='《Половое воспитание》\nОценка 8/10\n2 сезона\n\nCтеснительный и необщительный подросток-девственник Отис живёт с мамой, которая работает секс-терапевтом. Объединившись с '
								                                            'одноклассницей Мэйв, Отис проводит сеансы терапии для своих сверстников, чтобы помочь им разобраться с неловкими и запутанными ситуациями.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-56.userapi.com/c857236/v857236905/1222f1/HB9KVPW6sV4.jpg')
							vk.messages.send(user_id=event.user_id, message='《13 причин почему》\nОценка 7/10\n3 сезона\n\nОднажды Клэй Дженсен находит на пороге своего дома коробку с аудиокассетами, записанными Ханной Бейкер. Он был влюблен в '
								                                            'эту девушку в школе, пока она однажды не покончила жизнь самоубийством. В своих записях Ханна указала 13 причин, которые толкнули её на это. И Клэй - одна из них.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-64.userapi.com/c205716/v205716905/af566/Q1THKWq1alA.jpg')
							vk.messages.send(user_id=event.user_id, message='《Оранжевый хит сезона》\nОценка 7/10\n7 сезонов\n\nПайпер Чепмен - обычная жительница Коннектикута. Она любит свою благополучную жизнь и все её приятные мелочи. '
																	        'Душ по утрам, красивый завтрак, занятия любовью. Но случается так, что благодаря своему мимолетному увлечению крупным наркоторговцем, Пайпер оказывается заключенной в '
																	        'тюрьму на долгие пятнадцать месяцев. Отныне ей необходимо не только привыкнуть к новому окружению, но и просто - выжить.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-59.userapi.com/c206728/v206728905/b036a/UY-B2bMxMOM.jpg')
							vk.messages.send(user_id=event.user_id, message='《Чернобыль》\nОценка 9/10\n1 сезон\n\n26 апреля 1988 года химик Валерий Легасов, надёжно спрятав шесть аудиокассет со своими воспоминаниями, вешается у себя в квартире. '
								                                            '26 апреля 1986 года в 1:23:45 во время проведения эксперимента по безопасности на Чернобыльской АЭС происходит взрыв реактора и пожар. Поднятые по тревоге пожарные без спецзащиты '
								                                            'прибывают на место аварии, не подозревая, что оказались в эпицентре крупнейшей в истории человечества техногенной катастрофы. Руководство ЧАЭС уверяет Кремль, что ситуация под контролем, '
								                                            'и радиационный фон в норме, но по настоянию академика Легасова его вместе с зампредседателя Совета Министров Борисом Щербиной отправляют разобраться в происходящем на месте.',
																			attachment=photo, random_id=get_random_id())
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Детектив', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фантастика', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Ужасы', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Выберите жанр сериала:', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms == 'фантастика' or vksms == 'фантастики':
							vk.messages.send(user_id=event.user_id, message='👀Вот, какие сериалы на жанр "Фантастика" у меня есть:' + sub, random_id=get_random_id())
							photo = add_photo('https://sun9-71.userapi.com/c205820/v205820909/b3b82/oVUPazP5Pc8.jpg')
							vk.messages.send(user_id=event.user_id, message='《Видоизменненый углерод》\nОценка 7/10\n2 сезона\n\nЭкранизация одноимённого бестселлера Ричарда К. Моргана, действие которого происходит на Земле далёкого будущего. Ключевой '
							                                                'особенностью цивилизации стала возможность сохранять сознание и личность человека в цифровом виде — и переносить из тела в тело, поддерживая «вечную» жизнь. Сознание главного героя, '
							                                                'наёмника Такеси Ковача (Йоэль Киннаман), освобождается из виртуальной тюрьмы, где пробыло аж 250 лет, и помещается в новое тело, с детективным заданием от богача Банкрофта (Джеймс Пьюрфой). '
							                                                'Банкрофт прошедшие 250 лет путешествовал из тела в тело, и теперь хочет расследовать убийство своего последнего воплощения. Тема с перезаписью и сохранением сознания роднит историю с «Чёрным зеркалом», также нащупывающим штрихи '
							                                                'нашего будущего и иронизирующего над ним — однако «Видоизмененный углерод» гораздо ближе к фильмам-нуар. Фантастический антураж добавляет ему экзотики, но в центре событий всё тот же одинокий, страдающий герой и '
							                                                'экзистенциальные переживания человека, из смысла жизни которого здесь исключена ключевая составляющая — бренность бытия.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-50.userapi.com/c857428/v857428909/1ac1f8/8OwI8_hA7HI.jpg')
							vk.messages.send(user_id=event.user_id, message='《Черное зеркало》\nОценка 8/10\n5 сезонов\n\nСаркастичная антология рассказывает о мире самого ближайшего будущего, в котором информационные технологии в лице гаджетов и соцсетей незаметно внедрились в тело и сознание людей, теперь балансирующих между комфортом и ужасом такого существования. '
								                                            'Неизвестно, как долго продержится граница между виртуальным и реальным миром в действительности, но поразмышлять об этом (и испугаться) весьма любопытно.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-20.userapi.com/c857728/v857728909/1a0532/6AzTXOVU0AU.jpg')
							vk.messages.send(user_id=event.user_id, message='《Мандалорец》\nОценка 8/10\n1 сезон\n\nОдинокий мандалорец-наёмник живёт на краю обитаемой галактики, куда не дотягивается закон Новой Республики. '
							                                                'Представитель некогда могучей расы благородных воинов теперь вынужден влачить жалкое существование среди отбросов общества.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-43.userapi.com/c857532/v857532909/1ad61e/20APZ5M5E50.jpg')
							vk.messages.send(user_id=event.user_id, message='《Отбросы》\nОценка 8/10\n5 сезонов\n\nКелли, Нейтан, Кертис, Алиша и Саймон выполняют общественные работы за совершение мелких преступлений. Они – не друзья. Более того, у них нет ничего общего. В группе постоянно происходят '
								                                            'конфликты, споры и драки. Но в удивительный день во время сильного шторма сильная молния делает из них супергероев и наделяет их сверхспособностями. Они понятия не имеют, что делать с открывшимися перспективами. Более того, никто '
								                                            'из них не рад своей новой силе, потому что она раскрывает их самые глубокие комплексы и тайны, которые бы они не хотели выставлять напоказ.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-37.userapi.com/c206728/v206728909/b2691/V-S8LJ0NqtM.jpg')
							vk.messages.send(user_id=event.user_id, message='《Рассказ служанки》\nОценка 8/10\n4 сезона\n\nДействие разворачивается в будущем, в республике Гилеад, где у власти стоят военные. В стране жестокие порядки и нравы, уважением в обществе пользуются только офицеры и их жёны. '
							                                                'Помимо тоталитарного устройства общества, в мире будущего есть серьёзная проблема — бесплодие. Лишь каждая сотая женщина способна к воспроизведению потомства. Чтобы продолжить офицерский род, семьи берут в дом служанку - суррогатную '
							                                                'мать из числа простых женщин, способных к деторождению. Исполнив долг, служанка должна расстаться со своим ребёнком и перейти на службу к новым хозяевам.',
																			attachment=photo, random_id=get_random_id())
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Детектив', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фантастика', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Ужасы', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Выберите жанр сериала:', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms == 'фэнтези':
							vk.messages.send(user_id=event.user_id, message='👀Вот, какие сериалы на жанр "Фэнтези" у меня есть:' + sub, random_id=get_random_id())
							photo = add_photo('https://sun9-12.userapi.com/c857324/v857324260/123a76/1Q6qbtGFXac.jpg')
							vk.messages.send(user_id=event.user_id, message='《Благие знамения》\nОценка 8/10\n1 сезон\n\nВ центре сюжета ангел Азирафель и демон Кроули, которые объединяют усилия, '
							                                                'чтобы предотвратить конец света, так как за долгие века успели привыкнуть к жизни на земле.\nСериал балует зрителя не '
							                                                'только нескучным сюжетом, но и пасхалками: библейскими, естественно, историческими и поп-культурными, так что любителям '
							                                                'подмечать отсылочки будет, чем занять свой пытливый взор. Кроме того, мини-сериал пропитан изящным английским юмором, '
							                                                'как бисквит коньяком, и природное обаяние главных актеров – британцев – тоже опьяняет. Любителям неприрывного экшена '
							                                                '«Благие знамения» могут показаться тяжеловатыми, но попробовать все же рекомендуем: остроумно, глубоко, свежо, так еще стильно и красиво в придачу.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-58.userapi.com/c205728/v205728260/b3865/ZWxUhBfl9IY.jpg')
							vk.messages.send(user_id=event.user_id, message='《Сверхестественное》\nОценка 8/10\n15 сезонов\n\nПолузабытые мифы и легенды американских городов оживают и пытаются убить '
							                                                'всех окружающих, да и вообще вокруг происходит что-то невообразимое и жуткое. Но, к счастью, братья Винчестеры уже паркуются где-то '
							                                                'за углом и решают все проблемы нашего мира. Сериал потребует внушительных затрат времени на просмотр и, но в 2020 году, спустя '
							                                                'пятнадцать лет на телеэкранах, «Сверхъестественное» официально заканчивается, и у зрителей появится возможность увидеть финал истории '
							                                                'охотников на демонов.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-41.userapi.com/c857320/v857320260/12807c/XU795S3aTcc.jpg')
							vk.messages.send(user_id=event.user_id, message='《Игра престолов》\nОценка 9/10\n8 сезонов\n\nПеснь льда и пламени» – серия книг, по которым снят сериал, основанная во многом на реальных '
							                                                'исторических событиях и также подпитанная идеями его величества Толкиена, поэтому и сериал представляет собой качественный фэнтези-продукт о борьбе за власть, '
							                                                'о пороках и добродетелях правителей и о том, как за все это платит народ.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-14.userapi.com/c858136/v858136260/1a010d/pRtpxpbK7qE.jpg')
							vk.messages.send(user_id=event.user_id, message='《Однажды в сказке》\nОценка 8/10\n7 сезонов\n\nСюжет фэнтези разворачивается в двух мирах - современном и сказочном. Жизнь 28-летней Эммы Свон меняется, когда ее 10-летний сын Генри, '
							                                                'от которого она отказалась много лет назад, находит Эмму и объявляет, что она является дочерью Прекрасного Принца и Белоснежки. Само собой разумеется, у мальчишки нет никаких сомнений, '
							                                                'что параллельно нашему существует альтернативный сказочный мир – город Сторибрук, в котором в итоге оказывается Эмма. Постепенно героиня привязывается к необычному мальчику и странному '
							                                                'городу, жители которого «забыли», кем они были в прошлом. А все из-за проклятия Злой Королевы (по совместительству приемной матери Генри), с помощью которого колдунья остановила время в '
							                                                'сказочной стране. Однако стоит протянуть руку - и сказка оживет. Эпическая битва за будущее двух миров начинается, но, чтобы одержать победу, Эмме придется принять свою судьбу',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-2.userapi.com/c206616/v206616260/af3e4/D8exFceoMrg.jpg')
							vk.messages.send(user_id=event.user_id, message='《Дневники вампира》\nОценка 8/10\n8 сезонов\n\nПрошло всего четыре месяца после трагической аварии, в которой погибли их родители, и 17-летняя Елена Гилберт и ее 15-летний брат Джереми все еще '
							                                                'пытаются оправиться от потери и вернуться к нормальной жизни. Елена всегда была отличной ученицей, красивой и популярной девушкой в школе, но теперь ей очень тяжело скрывать свою печаль от внешнего мира. '
							                                                'В начале учебного года внимание Елены и ее друзей привлекает новый ученик, загадочный и красивый Стефан Сальваторе. Стефан и Елена тут же чувствуют взаимную симпатию, но Елена даже не подозревает, что Стефан – '
							                                                'вампир, которому уже сотни лет, и который старается мирно жить среди людей, несмотря на то, что его брат, Дэймон – воплощение вампирской жестокости и кровожадности. Теперь два брата-вампира – один добрый, другой '
							                                                'злой – ведут борьбу за души Елены, ее друзей и других жителей городка Мистик Фоллз.',
																			attachment=photo, random_id=get_random_id())
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Детектив', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фантастика', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Ужасы', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Выберите жанр сериала:', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms == 'ужас' or vksms == 'ужасы'  or vksms == 'ужастик' or vksms == 'ужастики':
							vk.messages.send(user_id=event.user_id, message='👀Вот, какие сериалы на жанр "Ужасы" у меня есть:' + sub, random_id=get_random_id())
							photo = add_photo('https://sun9-52.userapi.com/c858420/v858420914/1af717/D8rOdW9KT-4.jpg')
							vk.messages.send(user_id=event.user_id, message='《Очень странные дела》\nОценка 9/10\n3 сезона\n\n1980-е годы, тихий провинциальный американский городок. Благоприятное течение местной жизни нарушает '
							                                                'загадочное исчезновение подростка по имени Уилл. Выяснить обстоятельства дела полны решимости родные мальчика и местный шериф, также события затрагивают '
							                                                'лучшего друга Уилла – Майка. Он начинает собственное расследование. Майк уверен, что близок к разгадке, и теперь ему предстоит оказаться в эпицентре ожесточенной '
							                                                'битвы потусторонних сил.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-20.userapi.com/c857620/v857620914/1b2fed/RAmbUobLWCg.jpg')
							vk.messages.send(user_id=event.user_id, message='《Леденящие душу приключения Сабрины》\nОценка 9/10\n3 сезона\n\nВедьма Сабрина пытается найти истинную себя между натурами смертной и ведьмы, при этом ей придётся '
							                                                'противостоять злым силам, которые угрожают ей, её семье и всему миру людей.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-32.userapi.com/c205716/v205716914/b01a8/JajWjlKPC2w.jpg')
							vk.messages.send(user_id=event.user_id,message='《Ходячие мертвецы》\nОценка 8/10\n11 сезонов\n\nСериал рассказывает историю жизни семьи шерифа после того, как «зомби» - эпидемия апокалиптических масштабов захлестнула земной шар. Шериф Рик Граймс '
																	        'путешествует со своей семьей и небольшой группой выживших в поисках безопасного места для жизни. Но постоянный страх смерти каждый день приносит тяжелые потери, заставляя героев почувствовать глубины '
								                                            'человеческой жестокости. Рик пытается спасти свою семью, и открывает для себя, что всепоглощающий страх тех, кто выжил, может быть опаснее бессмысленных мертвецов, бродящих по земле.',
																	   		 attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-14.userapi.com/c858320/v858320914/1af5cd/w5RKXhK0xbA.jpg')
							vk.messages.send(user_id=event.user_id, message='《Ведьмак》\nОценка 7/10\n1 сезон\n\nВедьмак Геральт, мутант и убийца чудовищ, на своей верной лошади по кличке Плотва путешествует по Континенту. За тугой мешочек чеканных монет этот мужчина избавит вас '
								                                            'от всякой настырной нечисти - хоть от чудищ болотных, оборотней и даже заколдованных принцесс. В сельской глуши местную девушку Йеннифэр, которой сильно не повезло с внешностью, зато посчастливилось иметь '
								                                            'способности к магии, отец продаёт колдунье в ученицы. А малолетняя наследница королевства Цинтра по имени Цири вынуждена пуститься в бега, когда их страну захватывает империя Нильфгаард. Судьбы этих троих '
								                                            'окажутся тесно связаны, но скоро сказка сказывается, да не скоро дело делается.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-10.userapi.com/c857532/v857532260/1a6a9b/1hMXWF8yypc.jpg')
							vk.messages.send(user_id=event.user_id, message='《Американская история ужасов》》\nОценка 8/10\n13 сезонов\n\nПервый сезон сериала сосредоточен на семействе Хармонов, которые переезжают из Бостона в Лос-Анджелес, чтобы начать новую жизнь, и поселяются в '
							                                                'старинном отреставрированном особняке, не представляя, что его предыдущие жильцы так и не нашли покоя после смерти. Второй сезон рассказывает совершенно другую историю — действие разворачивается вокруг журналистки, '
							                                                'которая приехала в психбольницу для душевнобольных преступников в надежде отснять репортаж о новоприбывшем маньяке «Кровавый лик», беспощадно убивавшем случайных женщин. В третьем сезоне речь идет о шабаше ведьм, '
							                                                'замаскированном под элитный пансион для «одаренных» девушек, который пытается защитить последних представительниц этого вида от вымирания. Сюжет четвёртого сезона вращается вокруг одного из последних «Цирков уродов» '
							                                                'в 1950-х годах. События пятого сезона происходят в большом позабытом многими отеле в центральной части Лос-Анджелеса. Этот отель скрывает в своих стенах множество секретов. Шестой сезон рассказывает о паре из Калифорнии, '
							                                                'которая переезжает в новый дом, где странные и паранормальные явления начинают преследовать их. Седьмой сезон рассказывает о президентских выборах в США 2016 года. В восьмом сезоне происходит апокалипсис. Несколько '
							                                                'стран запустили ядерные ракеты, уничтожившие большую часть населения Земли. Избранным счастливчикам посчастливилось укрыться в бункере.',
																			attachment=photo, random_id=get_random_id())
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Детектив', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фантастика', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Ужасы', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Выберите жанр сериала:', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						else:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Детектив', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фантастика', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Ужасы', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Извини, я не знаю такого жанра', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				elif idslov[event.user_id] == 'l_films':
					if out_game(vksms):
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Сериалы', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Фильмы', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Аниме', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Выберите категорию:', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'l_menu'
					else:
						if vksms == 'детектив' or vksms == 'детективы':
							vk.messages.send(user_id=event.user_id, message='👀Вот, какие фильмы на жанр "Детектив" у меня есть:' + sub, random_id=get_random_id())
							photo = add_photo('https://sun9-18.userapi.com/c857336/v857336301/13431e/vEeU5LLZ1F8.jpg')
							vk.messages.send(user_id=event.user_id, message='《Убийство в Восточном экспрессе》\nОценка 7/10\n\nПутешествие на одном из самых роскошных поездов Европы неожиданно превращается в одну из самых стильных и захватывающих загадок в истории. Фильм рассказывает историю тринадцати пассажиров поезда, '
							                                                'каждый из которых находится под подозрением. И только сыщик должен как можно быстрее разгадать головоломку, прежде чем преступник нанесет новый удар.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-57.userapi.com/c853528/v853528301/20ad8d/mSlEMjwVBgY.jpg')
							vk.messages.send(user_id=event.user_id, message='《Достать ножи》\nОценка 9/10\n\nНа следующее утро после празднования 85-летия известного автора криминальных романов Харлана Тромби виновника торжества находят мёртвым. Налицо - явное самоубийство, но полиция по протоколу опрашивает всех '
							                                                'присутствующих в особняке членов семьи, хотя, в этом деле больше заинтересован частный детектив Бенуа Блан. Тем же утром он получил конверт с наличными от неизвестного и заказ на расследование смерти Харлана. Не нужно быть опытным следователем, '
							                                                'чтобы понять, что все приукрашивают свои отношения с почившим главой семейства, но Блану достаётся настоящий подарок - медсестра покойного, которая физически не выносит ложь.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-9.userapi.com/c853624/v853624301/2140a1/0duI4TPtCRI.jpg')
							vk.messages.send(user_id=event.user_id, message='《Нэнси Дрю и потайная лестница》\nОценка 8/10\n\nПосле смерти жены Карсон решает покинуть Чикаго и начать новую жизнь со своей дочерью в Ривер-Хайтс. Вот только 16-летней Нэнси жить в маленьком городке довольно скучно, поэтому она постоянно '
							                                                'ищет себе развлечение. Спустя некоторое время девушка решает помочь пожилой женщине, которая живет в старом доме, где происходят странные вещи. Чтобы лучше разобраться в происходящем, Нэнси отправляется на ночевку к своей новой знакомой и '
							                                                'становится свидетелем пугающих событий: двери открываются и закрываются сами по себе, вещи перемещаются по воздуху, а таинственная фигура в плаще предупреждает девушку об опасности.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-55.userapi.com/c205624/v205624938/c0c94/QAIg9yPzjTc.jpg')
							vk.messages.send(user_id=event.user_id, message='《Инферно》\nОценка 7/10\n\nПрофессор Роберт Лэнгдон приходит в сознание в одной из итальянских больниц, полностью потеряв память. Местный врач Сиенна Брукс пытается помочь Роберту не только восстановить воспоминания, но '
							                                                'и остановить загадочных злоумышленников, которые намерены распространить смертоносный вирус. Разгадка таинственной истории связана с «Адом» (ит. Inferno) - первой частью «Божественной комедии» Данте.',
								                             		     	attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-64.userapi.com/c855528/v855528193/2097b3/hAFgRvdnBW0.jpg')
							vk.messages.send(user_id=event.user_id, message='《Детектив Пикачу》\nОценка 8/10\n\nИстория начинается с таинственного исчезновения частного детектива экстра-класса Гарри Гудмана, расследовать которое предстоит его 21-летнему сыну Тиму. Помощь в расследовании ему окажет бывший партнер отца, детектив '
								                                            'Пикачу – уморительный, остроумный и обаятельный сыщик, который является загадкой даже для себя самого. Обнаружив, что они каким-то фантастическим образом способны общаться друг с другом, Тим и Пикачу объединяют усилия в захватывающем расследовании этой '
								                                            'запутанной истории. В погоне за уликами по неоновым улицам Райм Сити – современного разросшегося мегаполиса, где люди и покемоны живут бок о бок в гиперреалистичном мире игрового экшна, – они встречают самых разнообразных покемонов и раскрывают ужасный '
								                                            'заговор, который способен разрушить это мирное сосуществование и стать угрозой для всей вселенной покемонов.',
																			attachment=photo, random_id=get_random_id())
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Детектив', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фантастика & фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Ужасы', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Выберите жанр фильма:', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms == 'драмма' or vksms == 'драммы':
							vk.messages.send(user_id=event.user_id, message='👀Вот, какие фильмы на жанр "Драмма" у меня есть:' + sub, random_id=get_random_id())
							photo = add_photo('https://sun9-16.userapi.com/c205716/v205716261/b1984/APJ6MwOiCxs.jpg')
							vk.messages.send(user_id=event.user_id, message='《Полночное солнце》\nОценка 7/10\n\nНочами 17-летняя Кэти сочиняет красивые песни под гитару, а днем она вынуждена скрываться во мраке: её нежная кожа не выносит солнечного света. '
							                                                'Но однажды в полночь Кэти знакомится с Чарли, веселым парнем с копной рыжих как солнце волос и очаровательной улыбкой. Внезапная и страстная любовь яркой вспышкой озаряет жизнь больной '
							                                                'девушки. И теперь ради возлюбленного она готова сгореть в лучах света безумного чувства.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-30.userapi.com/c854528/v854528261/2188d5/ze9ec0xbYAE.jpg')
							vk.messages.send(user_id=event.user_id, message='《Маленькие женщины》\nОценка 8/10\n\nИстория взросления четырёх непохожих друг на друга сестер. Где-то бушует Гражданская война, но проблемы, с которыми сталкиваются девушки, актуальны '
							                                                'как никогда: первая любовь, горькое разочарование, томительная разлука и непростые поиски себя и своего места в жизни.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-41.userapi.com/c205824/v205824261/b28e0/0UGpAGeC6lI.jpg')
							vk.messages.send(user_id=event.user_id, message='《С любовью,Рози》\nОценка 8/10\n\nРози и Алекс были лучшими друзьями с детства, и теперь, по окончании школы, собираются вместе продолжить учёбу в университете. Однако в их судьбах '
							                                                'происходит резкий поворот, когда после ночи со звездой школы Рози узнаёт, что у неё будет ребенок. Невзирая на то, что обстоятельства и жизненные ситуации разлучают '
							                                                'героев, они и спустя годы продолжают помнить друг о друге и о том чувстве, что соединило их в юности…',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-43.userapi.com/c857028/v857028261/12a56e/EDGxl7Ryxzc.jpg')
							vk.messages.send(user_id=event.user_id, message='《Назови меня своим именем》\nОценка 8/10\n\n1983 год, Италия. Элио семнадцать, и это лето он проводит на вилле у родителей, американского профессора и переводчицы-итальянки. '
							                                                'Юноша c детства начитанный и любознательный, Элио разбавляет обычные летние занятия вроде купания в море и ленивого флирта с подругой Марцией чтением и транскрибированием классической музыки. '
							                                                'В один прекрасный день, впрочем, безмятежность летнего отдыха нарушает приезд Оливера – молодого американского учёного, ассистента отца Элио.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-51.userapi.com/c857524/v857524261/1af80c/fsXTq3ieRcY.jpg')
							vk.messages.send(user_id=event.user_id, message='《Богемская расподия》\nОценка 8/10\n\nЧествование группы Queen, их музыки и их выдающегося вокалиста Фредди Меркьюри, который бросил вызов стереотипам и победил условности, чтобы стать одним из '
							                                                'самых любимых артистов на планете. Фильм прослеживает головокружительный путь группы к успеху благодаря их культовым песням и революционному звуку, практически распад коллектива, поскольку образ '
							                                                'жизни Меркьюри выходит из-под контроля, и их триумфальное воссоединение накануне концерта Live Aid, ставшим одним из величайших выступлений в истории рок-музыки.',
																			attachment=photo, random_id=get_random_id())
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Детектив', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фантастика & фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Ужасы', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Выберите жанр фильма:', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms == 'ужас' or vksms == 'ужасы' or vksms == 'ужастик' or vksms == 'ужастики':
							vk.messages.send(user_id=event.user_id,
								message='👀Вот, какие фильмы на жанр "Ужасы" у меня есть:' + sub,
								random_id=get_random_id())
							photo = add_photo('https://sun9-70.userapi.com/c855736/v855736623/2113c4/RZ6a0VrhKy8.jpg')
							vk.messages.send(user_id=event.user_id, message='《Сплит》\nОценка 7/10\n\nCредь бела дня с многолюдной парковки незнакомец похищает трёх школьниц. Они приходят в себя в закрытом помещении, а в душе владельца таятся 23 лика страха. Сменяя друг друга, '
								                                            'личности ведут обычную для них жизнь - работают и ходят к психотерапевту, периодически напоминая пленницам, что они дожидаются 24-ю личность, которая скоро явит себя миру.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-46.userapi.com/c205820/v205820623/bf20b/Ae9Nfy1LiGk.jpg')
							vk.messages.send(user_id=event.user_id, message='《Солнцестояние》\nОценка 7/10\n\nДень летнего солнцестояния – древний праздник, который во всех культурах окутан мистическим ореолом. В отрезанном от цивилизованного мира шведском поселении в этот день '
							                                                'проводятся уникальные обряды с многовековой традицией. Именно туда отправляется группа молодых американских студентов-антропологов, прихватив с собой девушку одного из них. Однако вскоре после прибытия друзья выясняют, что местные обряды далеко не безобидны.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-13.userapi.com/c855028/v855028623/211a40/cBjP_FUGhFc.jpg')
							vk.messages.send(user_id=event.user_id, message='《Страшные истории для рассказа в темноте》\nОценка 8/10\n\nХэллоуин 1968 года. Старшеклассница Стелла, большая любительница страшных историй, и двое её друзей наряжаются в нелепые костюмы и идут гулять. Так получается, что ребята выводят '
							                                                'из себя школьного задиру и хулигана Томми и, спасаясь от него, знакомятся с неместным парнем Рамоном, а после отправляются в старинный заброшенный особняк. Дом принадлежал семье Бэллоуз, все члены которой загадочно исчезли почти 100 лет назад, '
							                                                'а про дочь семейства Сару до сих пор ходят жуткие легенды - якобы она может убивать, рассказывая истории. Друзья находят потайную комнату, и Стелла забирает домой книгу, где Сара писала свои рассказы, и на страницах которой этим же вечером появится новый, а'
							                                                ' хулиган Томми исчезнет без следа.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-23.userapi.com/c857020/v857020623/1344b7/JuBo9t2x-ec.jpg')
							vk.messages.send(user_id=event.user_id, message='《Счастливого дня смерти》\nОценка 8/10\n\nКаждый в универе мечтал попасть на её день рождения, но праздник был безнадежно испорчен незнакомцем в маске, убившим виновницу торжества. Однако судьба преподнесла имениннице леденящий душу подарок – '
							                                                'бесконечный запас жизней. И теперь у девушки появился шанс вычислить своего убийцу, ведь этот день будет повторяться снова и снова.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-43.userapi.com/c205816/v205816623/b1099/EmzI_fqUlNg.jpg')
							vk.messages.send(user_id=event.user_id, message='《Проклятие монахини》\nОценка 9/10\n\nКогда в уединенном монастыре в Румынии молодая монахиня совершает самоубийство, Ватикан отправляет расследовать происшествие священника с туманным прошлым и послушницу на пороге невозвратных обетов. '
							                                                'Рискуя не только жизнями, но и своими душами, они сталкиваются со злобной силой, принявшей облик демонической монахини, а монастырь становится полем битвы между живыми и проклятыми.',
																			attachment=photo, random_id=get_random_id())
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Детектив', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фантастика & фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Ужасы', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Выберите жанр фильма:', random_id=get_random_id(), keyboard=keyboard.get_keyboard())

						elif vksms.count('фэнтези') > 0 or vksms.count('фантастик') > 0:
							vk.messages.send(user_id=event.user_id,
								message='👀Вот, какие фильмы на жанр "Фэнтези" & "Фантастика" у меня есть:' + sub,
								random_id=get_random_id())
							photo = add_photo('https://sun9-4.userapi.com/c858224/v858224193/1b9641/uyp-iMeQTDQ.jpg')
							vk.messages.send(user_id=event.user_id, message='《Мстители》\nОценка 9/10\n\nЛоки, сводный брат Тора, возвращается, и в этот раз он не один. Земля на грани порабощения, и только лучшие из лучших могут спасти человечество.\nНик Фьюри, глава международной организации Щ. И. Т. , собирает выдающихся '
							                                                'поборников справедливости и добра, чтобы отразить атаку. Под предводительством Капитана Америки Железный Человек, Тор, Невероятный Халк, Соколиный глаз и Чёрная Вдова вступают в войну с захватчиком.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-34.userapi.com/c857732/v857732193/1a8dc1/jsn-PSwg94I.jpg')
							vk.messages.send(user_id=event.user_id, message='《Аквамен》\nОценка 7/10\n\nДействие фильма разворачивается в необъятном и захватывающем подводном мире семи морей, а сюжет знакомит зрителей с историей происхождения получеловека-полуатланта Артура Карри и ключевыми событиями его жизни – '
							                                                'теми, что заставят его не только столкнуться с самим собой, но и выяснить, достоин ли он быть тем, кем ему суждено… царем',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-14.userapi.com/c857332/v857332193/bb709/ywXFO5SFaNo.jpg')
							vk.messages.send(user_id=event.user_id, message='《Джуманджи: Зов джунглей》\nОценка 8/10\n\nЧетверо подростков оказываются внутри игры Джуманджи. Их ждет схватка с носорогами, черными мамбами, а на каждом шагу будет подстерегать бесконечная череда ловушек и головоломок. В игре они перевоплощаются: '
							                                                'робкий и застенчивый Спенсер превращается в отважного и сильного исследователя, здоровяк Фридж – в коротышку-зоолога, модница и красавица Беттани – в полного профессора, а неуклюжая Марта становится бесстрашной и ловкой амазонкой. '
							                                                'Друзьям придется привыкнуть к новым ролям, постараться не погибнуть и найти дорогу домой.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-56.userapi.com/c206724/v206724193/bf7a8/6JtJFOwp_bc.jpg')
							vk.messages.send(user_id=event.user_id, message='《Алладин》\nОценка 7/10\n\nМолодой воришка по имени Аладдин хочет стать принцем, чтобы жениться на принцессе Жасмин. Тем временем визирь Аграбы Джафар намеревается захватить власть над Аграбой, а для этого он стремится заполучить волшебную лампу, '
							                                                'хранящуюся в пещере чудес, доступ к которой разрешен лишь тому, кого называют «алмаз неограненный», и этим человеком является не кто иной, как сам Аладдин.',
																			attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun9-58.userapi.com/c858436/v858436301/1aeb28/IXHiCHIjNlc.jpg')
							vk.messages.send(user_id=event.user_id, message='《Ветреная река》\nОценка 8/10\n\nВ пустыне на территории индейской резервации «Ветреная река» егерь Кори Ламберт находит изувеченное тело молодой девушки. Начинающий агент ФБР, которая не знакома с '
								                                            'местными природными условиями и обычаями, просит охотника из Департамента рыболовства и охоты помочь поймать убийц девушки.',
																			attachment=photo, random_id=get_random_id())
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Детектив', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фантастика & фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Ужасы', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Выберите жанр фильма:', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				elif idslov[event.user_id] == 'l_anime':
					if out_game(vksms):
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Сериалы', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Фильмы', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Аниме', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Выберите категорию:',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'l_menu'
					else:
						if vksms.count('приключен') > 0:
							vk.messages.send(user_id=event.user_id,
								message='👀Вот, какое аниме на жанр "Приключения" у меня есть:' + sub,
								random_id=get_random_id())
							photo = add_photo('https://sun1-97.userapi.com/8JyqLtdVgakavRE-Uvryl8TkgGgyimIa0vUKrA/P0wUzJCd85I.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Война двенадцати》\nОценка 8.26/10\n\nДвенадцать войнов, наделённых силами животных восточного календаря, сражаются друг с другом, рискуя собственными жизнью и гордостью. И всё ради исполнения одного единственного желания.',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-99.userapi.com/gLjC-vAu8Cy0HaoCIG7MoURjhr9B9syyu0GLwA/GJ2sWJIoq6M.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Военная хроника маленькой девочки》\nОценка 9.15/10\n\nНа передовой сражается маленькая девчонка. Светлые волосы, голубые глаза, фарфоровое личико — её зовут Таня Дегречова, и её приказов, отданных слегка шепелявым голосом, '
								        'слушается целый отряд. В действительности, она — одна из самых лучших офисных работников Японии, которая была перерождена в этом теле, ненароком перейдя дорогу таинственному созданию, именуемому себя Богом. И эта маленькая '
								        'девчонка, ставящая карьеру и тяжкий труд превыше всего, станет настоящим кошмаром для волшебников императорской армии.',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-93.userapi.com/Ra4NOBH6fJPOhRlUYHnfiluUmsxjCe19gRgwiQ/BGiI0u9vXCg.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Скитальцы》\nОценка 9.28/10\n\nТоёхиси Симадзу является одним из лучших мечников эпохи Сэнгоку. В одном из сражений он получает сильное ранение и уже готовится покинуть мир живых, как неожиданно для себя оказывается в '
								        'таинственном месте, где его ожидает человек по имени Мурасаки. Незнакомец направляет искалеченного героя в параллельный мир, в котором все не так спокойно. Войны, которые не уступающие по масштабу земным, царят на этой земле, '
								        'и Симадзу оказывается в самом центре событий. Но помимо нашего протагониста, сюда были направлены другие войны Земли. Волею судьбы наш герой становится частью группировки «Скитальцы», так начинается его новая жизнь в неизведанном мире.',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-27.userapi.com/GVNfRu5prwjjbAKlUiAr0lJOvsv9XTMZ9JxA0w/85RvBkCg8yM.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Сказание об Арслане》\nОценка 9.05/10\n\nПроцветающий город Экбатана, стоящий на сухопутных торговых путях, был столицей великой империи, чья армия раз за разом отражала атаки соседей и защищала ее народ и богатства. Юного принца Арислана '
								        'с младых ногтей готовили к роли нового правителя, однако завоевывать сердца окружающих у него, выросшего в тени безжалостного отца и отстраненной матери, получалось намного лучше, чем постигать военное искусство. Когда Арислану исполнилось '
								        'четырнадцать лет, он принял участие в первом военном походе, который обернулся катастрофой – его отца предали, и армия, которую вел Арислан, попала в ловушку врага. Спасенный бесстрашным воином и преданным другом, Арислан начал путешествие, '
								        'которое должно было сделать его настоящим королем – великим, решительным и справедливым. Ведь у принца, мало оправдывающего ожидания родителей, было то, чего лишены многие правители: доброе сердце и открытый разум, позволяющие преодолеть силу '
								        'традиций и старые предрассудки, чтобы увидеть большой и многообразный мир таким, каков он есть.',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-29.userapi.com/FpOOxXJvkI7n6bDYGjQXxkyO5L-2_elDTk62RA/bGG0WEyHDkU.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Империя Альтаир》\nОценка 9.12/10\n\nТогрул Махмуд - юный паша, преданно служащий своей стране, над которой начинают сгущаться тучи войны из-за угрозы нападения со стороны агрессивно настроенной Империи. Да и внутри государства не все гладко, '
								        'население разделилось на пацифистов и тех, кто жаждет войны.\nМахмуд отправляется в поход, чтобы сохранить мир любой ценой. Всё глубже и глубже погружаясь в политические интриги древнего мира, он обретает как друзей так и врагов. Но кто возьмёт '
								        'вверх? И что сделает Махмуд, если война станет станет неизбежна?',
								attachment=photo, random_id=get_random_id())
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Приключения', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Мафия', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Мистика', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Выберите жанр аниме:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms == 'драмма' or vksms == 'драммы':
							vk.messages.send(user_id=event.user_id,
								message='👀Вот, какое аниме на жанр "Драмма" у меня есть:' + sub,
								random_id=get_random_id())
							photo = add_photo('https://sun1-14.userapi.com/RvMvQXV9Bsk7lNhMmhzYDhqfWWrR7h-DJLsSsQ/2BlEe9hAU-I.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Токийский гуль》\nОценка 8.79/10\n\nСтудент университета Канеки Кен в результате несчастного случая попадает в больницу, где ему по ошибке пересаживают '
								        'органы одного из гулей - чудовищ, питающихся человеческой плотью. Теперь он сам становится одним из них, а для людей превращается в изгоя, подлежащего уничтожению. '
								        'Но сможет он ли стать своим для других гулей? Или теперь в мире для него больше нет места? Аниме расскажет о судьбе Канеки и том, какое влияние он окажет на '
								        'будущее Токио, где идет непрерывная война между двумя видами.',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-93.userapi.com/RE23_ys_0k5j_nHfSUgGmGtFEKsh6Ge8R23rzg/r79kKE3UZaE.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Парад Смерти》\nОценка 9.19/10\n\nДействия сериала разворачиваются в баре под названием «Quindecim», ничем не примечательном на первый взгляд. '
								        'Посетителями этого бара поневоле становятся люди, которые уже умерли, но ещё не попали ни в рай, ни в ад. Управляющий заведением, а по совместительству и '
								        'бармен по имени Дэким предлагает посетителям сыграть в игру, где ставкой будет их жизнь (что многих поначалу шокирует, но так как они не имеют права '
								        'отказаться от игры, у них просто нет выбора), и выяснить, кто достоин перерождения, а кто отправится в небытие.',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-93.userapi.com/sJCsUVLOhOdWwbG8F8jHj5a3TxFAuRp0bfexOA/OAo_Y5wfF4w.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Восхождение героя щита》\nОценка 9.09/10\n\nИстория повествует о параллельном мире «Мельмарк», которое постоянно подвергается атакам темных сил. '
								        'Для сохранения баланса между мирами, в нашу вселенную был послан призыв о помощи. В ответ на зов в фантастические края отправляются четыре героя из '
								        'современной Японии, где персонажи овладевают легендарными видами оружия: мечом, копьем, луком и щитом.\nВ параллельном мире, из-за отсутствия '
								        'атакующих возможностей своего оружия, «Герой Щита» оказывается самым слабым персонажем. Отаку Наофуми Иватани располагает к себе только одного '
								        'союзника, прекрасную принцессу Мальти Мельромарк. Однако вскоре она предает Наофуми, украв все богатства, и заявляет, что была похищена и изнасилована им.'
								        '\nЗа его предполагаемые преступления Наофуми воспринимается обществом как изгой и злодей. С ненавистью, наполняющей его сердце, он остается один '
								        'и клянется отомстить всем, кто его оклеветал.',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-96.userapi.com/EkbUAJq1aYWUBreW9dMKiDhf8jICYBmagewewQ/apNnQFxxpT0.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Отвергнутый священный зверь》\nОценка 7.66/10\n\nГражданская война поделила страну на две противоборствующие группы: Север и Юг. Южане, готовые '
								        'на всё ради победы, пустили в ход запретные технологии, превратив своих солдат в монстров. Те полностью утратили человеческий облик, получив взамен '
								        'нечеловеческую силу, и в итоге отвоевали свои земли.\nВойна закончена, однако это не принесло в страну мир и спокойствие. Магия, которая изменила '
								        'тела людей, не имела обратного действия, более того, они стали постепенно утрачивать человеческое сознание, так что солдаты, превращённые в монстров, '
								        'оказались не просто никому не нужны, а опасны. Народ, помня своих спасителей, всё же стал их бояться, избегать, а потом и вовсе уничтожать.\nОтец '
								        'главной героини тоже был превращён в монстра, а потом убит. Причём убит не на поле брани, а человеком, ставшим охотником за монстрами. Не смирившись '
								        'с потерей отца, Нэнси Шаал Бэнкрофт решает отомстить убийце. Она находит его и разряжает в него своё ружье. Однако тот остаётся цел и невредим, '
								        'потому что, как оказалось, он тоже монстр.\nЗовут его Хэнк, и он объясняет Нэнси, что убивает бывших собратьев по оружию не из жестокости, '
								        'а потому, что исполняет данную клятву. Хэнк предлагает Нэнси отправиться вместе с ним, чтобы она больше узнала о монстрах и о том, почему '
								        'будет лучше, если они погибнут от рук бывшего товарища.',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-92.userapi.com/DYODlbbaG9jQ3pii8PpGd_rT4sMChegtamyjcw/mWqERAIWCRo.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Последний Серафим》\nОценка 8.90/10\n\nГлавные герои истории Юичиро и Микаэла, сироты из приюта. Как фото-негатив друг друга они '
								        'столь же отличаются внутренне, сколь и внешне. Микаэла – добрый отзывчивый мальчик, готовый на любые жертвы ради приютских детей, которых '
								        'по общим правилам учреждения называет «семьей». Юичиро - противоположность Микаэла, непримиримый, всегда колкий бунтарь.\nСудьбе было мало '
								        'отобрать у детей все, вокруг них один за другим гибнут люди - страшный вирус неизвестного происхождения в одночасье уничтожает взрослое население. '
								        'Вампиры-аристократы в сложившейся ситуации пришли и взяли в руки контроль над уцелевшими. Дети для них - постоянный источник свежей крови, '
								        'которую тем приходится в обязательном порядке сдавать. Так Мика и Ю оказались заложниками закрытого Города вампиров. В этом перевернутом мире '
								        'остается только выживать, а не жить, но приютские друзья мечтают сбежать из заточения…\nДальнейшие события истории происходят спустя 4 года после побега.'
								        '\nДобро и зло, люди и вампиры, как белое и черное… между ними легко провести разделяющую черту. Но так ли очевидна эта черта, и кому можно доверять на самом деле?'
								        '\nСумеют ли главные герои сохранить в непримиримой войне между расами свою дружбу, покажет время…',
								attachment=photo, random_id=get_random_id())
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Приключения', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Мафия', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Мистика', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Выберите жанр аниме:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms == 'мафия' or vksms == 'мафиози':
							vk.messages.send(user_id=event.user_id,
								message='👀Вот, какое аниме на жанр "Мафия" у меня есть:' + sub,
								random_id=get_random_id())
							photo = add_photo('https://sun1-20.userapi.com/Wz6Tn_QRZL5CeBm4v46jZcUNsM2HHrH3zM5wtw/HcpgNnVakxA.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《91 день》\nОценка 9.22/10\n\nНа дворе 1920 год. В США действует сухой закон, который запрещает производство и сбыт алкогольной продукции, тем самым открывая для мафиозных семей новую нишу.\nВ центре этих событий юный '
								        'Анджело Лагуса, трагически потерявший своих родных в ходе междоусобиц внутри мафии. Ему удается скрыться от убийц и покинуть город. Но спустя годы, Анджело, потерявший всякий смысл жить, получает письмо от неизвестного '
								        'отправителя, в которое были вписаны имена людей, причастных к гибели его семьи. Теперь, Анджело, движимый жаждой мести отправляется в родной Лорэл с единственной целью - отплатить тем, кто забрал жизни членов его семьи...',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-18.userapi.com/IFjtBFzsa3nSVH3HS0np2dloJfs0MvBnbqatRg/RNEdbsXxMmQ.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Пираты Чёрной Лагуны》\nОценка 9.13/10\n\nПростой японский служащий Рокуро Окадзима отправляется в командировку в юго-восточную Азию: ему нужно доставить очень важный диск. Вся его жизнь переворачивается в тот момент, '
								        'когда на корабль нападают пираты и берут Рокуро в заложники. Спасая лицо, компания решает избавиться от диска вместе со служащим. Чтобы выжить, Рок объединяется с пиратами – и теперь он сотрудник «Чёрной лагуны»! '
								        'Вместе они сражаются с наемными убийцами, вертолетами и кораблями...',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-98.userapi.com/egmOpgFSL5Pb5AA4ieIyMsaLfDZbp_nV4Tv2dg/khfB734qUHc.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Бандитос》\nОценка 8.81/10\n\nУ вас течет кран? Отломалась ножка стула? Завелись тараканы? В предприимчивой Японии в таких случаях звонят в специальную контору, "мастерам на все руки", которые все починят, '
								        'со всем помогут, все проблемы решат. Называются такие мастера абстрактным словом "Бенрия-сан". Вот только где-то есть районы, где "бытовые" проблемы имеют широкий криминальный масштаб, а вредители крупные и '
								        'злобные двуногие, от которых "дрожат" даже иные тюрьмы. Вот на таких улицах и переулках вырастают свои "Бенрия-сан", которые так же без вопросов приведут любой объект хозяствования в состояние "нет проблем". '
								        'У вас все еще проблемы? Не раздумывая звоните Варрику и Николасу: приятная секретарша всегда ответит на звонок - и специалист немедленно отправится вам на помощь, прихватив кольт, катану и прочий рабочий инструмент.', attachment=photo,
								random_id=get_random_id())
							photo = add_photo('https://sun1-15.userapi.com/ahbQYiqcJf3Ppl7BmTm0InZJ4I-j_AAEaYCaJg/kd3TFfzZaa8.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Ёрмунгант》\nОценка 9.11/10\n\nКаждый в этом мире из чего-то стреляет: это может быть обычное ограбление с несколькими автоматами, а может быть локальная война, где участвует самое разнообразное оружие – '
								        'от танков до вертолётов и зенитных комплексов. О торговцах оружием и пойдёт речь в данном аниме, а именно о юной Коко – молодая, но решительная, она собрала удивительную команду профессионалов. Бывшие мафиози, '
								        'спецназовцы, полицейские, простые солдаты, которые раньше были по разным сторонам снайперского прицела сейчас работают ради одной цели и живут как настоящая семья.\nПоследним кто присоединился к такой разношёрстной '
								        'и многонациональной команде стал Йона – маленький солдат, обладающий удивительным хладнокровием. И теперь, превозмогая своё презрение к оружию, он будет использовать его ежедневно, '
								        'ведь только с помощью Коко он сможет отомстить за свою семью.',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-98.userapi.com/VdfqqBCFgHgLHKVIHv70ibncaO5auhUZtsUS6A/-kbq7IVDcgY.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Псы: Бродячие псы, воющие во тьме》\nОценка 8.31/10\n\nОдин город. Четыре истории. Четыре человека. Михай стар и сентиментален. Наото молода и безжалостна. Бадо легкомыслен и никотинозависим. '
								        'Гейне холоден и почти неуязвим. Что объединяет людей, чьи жизни так несхожи? Смерть. Смерть, которую они щедро раздают окружающим. Потому что все они – убийцы.',
								attachment=photo, random_id=get_random_id())
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Приключения', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Мафия', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Мистика', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Выберите жанр аниме:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())

						elif vksms.count('фэнтези') > 0:
							vk.messages.send(user_id=event.user_id,
								message='👀Вот, какое аниме на жанр "Фэнтези" у меня есть:' + sub,
								random_id=get_random_id())
							photo = add_photo('https://sun1-20.userapi.com/kdjNUV3LPzyNpWqcCbwjCTrv6O_Z2SRpB9BIMg/llErPgQmpEc.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Убийца Гоблинов》\nОценка 8.58/10\n\nЮная Жрица вступает в гильдию авантюристов. Благодаря своим навыкам она стала желанной гостьей в любой команде, даже несмотря на то, что как авантюрист представляла из себя совершенно '
								        'неопытного новичка.\nВ этом мире существует множество монстров. Среди всего их разнообразия гоблины считаются слабейшими и почти всегда становятся первой добычей для начинающих авантюристов. Руководствуясь этим знанием, '
								        'группа низкоранговых авантюристов вместе с присоединившейся к ним Жрицей отправилась на своё первое задание — «зачистку» логова гоблинов. Однако что-то пошло не по плану, и группа попала в большую беду. '
								        'В последний момент к ним на помощь пришёл таинственный мечник, облачённый в рыцарские доспехи. Вскоре собравшимся стало известно его имя — Убийца Гоблинов.\nПо возвращении в город Жрица решает присоединиться к своему '
								        'спасителю, вскоре после чего сталкивается с новыми загадками и тайнами, друзьями и врагами. Что ждёт её на этом пути? Что за человек скрывается под маской Убийцы Гоблинов? Почему он посвятил себя '
								        'уничтожению гоблинов? И так ли просты гоблины на самом деле?',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-15.userapi.com/tt6w3GpNucR9AhjcS0wXbHzIkW2QXY4t36lvfA/-QrZBc3lxH0.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Владыка》\nОценка 9.20/10\n\nИстория начинается с последнего дня существования популярной онлайн-игры «Иггдрасиль». Главный герой, Момонга, решил остаться в любимой игре до самого последнего момента. '
								        'Однако сервер не прекратил свою работу, и Момонга застревает в своем скелетоподобном персонаже и переносится в другой мир. Теперь "Могучему Владыке" придется открыть для себя новый мир и столкнуться с '
								        'многочисленными испытаниями.\nУ него нет ни родни, ни друзей, ни места под солнцем, но он приложит все усилия для того, чтобы завоевать новый мир!',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-19.userapi.com/p6_OmK4jYlq5Ddw0OTULfK-P8UCF8zgXBpayyQ/HDu3lWUnMg0.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《В подземелье я пойду, там красавицу найду!》\nОценка 8.94/10\n\nВ загадочном мире есть место под названием "Подземелье", входом в которое служил огромный город Орарио. Люди стремятся '
								        'туда за славой, честью, приходят, надеясь получить всё то, о чем мечтают. И именно здесь один парень-мечтатель встречается с маленькой богиней, не нашедшей ни одного '
								        'последователя. Сможет ли герой помочь девушке и при этом осуществить свои мечты?',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-88.userapi.com/oVoJuqO5xotoPandf5QIkGL3U0gLnqhNT97ktA/4T_boQb2lcw.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Легенда о Гранкресте》\nОценка 8.91/10\n\nВ стране, где правит Хаос, Лорды обладают силой святого герба, которая может противостоять Хаосу и защищать людей. Однако прежде чем кто-то '
								        'успел что-то осознать, правители отказались от своего кредо - очищать мир от хаоса - и начали сражаться друг с другом за власть.\nСирука - маг-одиночка, которая презирает Лордов. '
								        'Тео - странствующий рыцарь, который путешествует, чтобы однажды освободить свой родной город. Они заключают контракт, чтобы изменить их мир, и освободить его от войн и хаоса.',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-26.userapi.com/XjkBJXUS8Ey_7S45iBbRY9lDbR4TijQ4qpwScw/7o6Uc5L-8mw.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Дороро》\nОценка 9.27/10\n\nВ стране царит смута, и один из генералов жаждет во что бы то ни стало одержать победу в решающей битве, которая ни много ни мало сулит '
								        'ему трон всей страны. Для этого он решается на страшный грех и заключает сделку с двенадцатью демонами: те помогают ему выиграть бой, а он за это отдаёт каждому из '
								        'них одну из частей тела своего новорожденного сына. Обречённый на гибель мальчик, тем не менее, выживает благодаря помощи доктора, создавшего для него протезы-оружие. '
								        'Преданный собственным отцом, юноша ничего так не желает, как отомстить родителю, но для этого ему сперва необходимо убить каждого демона и вернуть отнятые части тела, '
								        'по одной за раз. На своём пути охоты и истребления демонов молодой человек встречает сироту Дороро, который утверждает, что является величайшим вором Японии. '
								        'Объединившись, они вместе отправляются в трудный путь, полный опасностей и приключений.',
								attachment=photo, random_id=get_random_id())
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Приключения', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Мафия', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Мистика', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Выберите жанр аниме:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms.count('мистика') > 0:
							vk.messages.send(user_id=event.user_id,
								message='👀Вот, какое аниме на жанр "Мистика" у меня есть:' + sub,
								random_id=get_random_id())
							photo = add_photo('https://sun1-99.userapi.com/hVeTL2q0bbAc0-1OqyXxwbm2MyOmgR5YH3LMVA/AVCN2ZOYvIc.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Темный дворецкий》\nОценка 8.9/10\n\nЧёрная комедия с элементами мистического триллера, судя по зашкаливающему количеству косплея по её мотивам на любом околоанимешном мероприятии, уже ставшая культовой. '
								        'Альтернативный взгляд на викторианскую Англию. Сиэль Фантомхайм – двенадцатилетний граф на службе Её Величества, владелец роскошного поместья, а также идеального дворецкого Себастьяна, которого он приобрёл в обмен на собственную душу. '
								        'Благодаря контракту с демоном Себастьян готов исполнить любой приказ своего господина, служит ему безупречным телохранителем и незаменимым помощником в любой ситуации. А в разнообразии этих ситуаций Сиэлю не откажешь. '
								        'Детективная история по расследованию убийства его родителей, борьба с итальянской мафией, тайные поручения королевы… «Кто, если не дворецкий семьи Фантомхайм, способен со всем этим справиться?»',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-88.userapi.com/kkaxjXWVUyw2NJP-Rkvo8i5fYJORH4bnEFfm_A/5ckt2_8IGpA.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Инспекторы чудес Ватикана》\nОценка 8.26/10\n\nВ этой истории рассказывается о гениальном учёном Джозефе Ко Хирага и эксперте в архивах и криптоанализе Роберто Николасе, которые работают в одной команде. Их прозвали "инспекторы чудес Ватикана", '
								        'ведь они путешествуют по миру и изучают подлинность разнообразных чудес.',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-26.userapi.com/dlRBcb97tjgptdBuuNZpqoFKJejBODsmdJrcfg/etgSs1eXd7Q.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Безумный Азарт》\nОценка 8.72/10\n\nЧастная академия Хяккао — место, где учится так называемая элита. Престижное учебное заведение для привилегированных особ с необычной программой обучения. Если ты ребёнок '
								        'богатейших из богатых, спортивные достижения или образованность не играют роли. Только умение читать своего оппонента или же владение искусством заключения сделок помогут здесь выжить. Что же отточит эти навыки лучше, чем строгий учебный план азартных игр? '
								        'В этой академии победители живут как короли, а проигравшие теряют всё. Но только с появлением Юмэко Джабами, ученики узнают, что значит по-настоящему играть!',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-86.userapi.com/msXXSM3qvDnlvWiBqbq6uH6fkB8Erf_-UlrXuQ/_Ny4cbnuN4c.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Оккультные служащие полуночи》\nОценка 8.22/10\n\nАрата Мияко недавно получил назначение в районный отдел регионального полуночного департамента по связям. В каждом из 23 районов Токио есть отдел занимающийся делами, связанными с '
								        'паранормальной активностью и оккультными практиками. У Арата есть особый дар — он может понимать нечеловеческую речь. В первый же свой рабочий день Арата сталкивается в парке с ёкаем, который принимает его за легендарного экзорциста эпохи Хэйан — Абэ-но Сэймэя.',
								attachment=photo, random_id=get_random_id())
							photo = add_photo('https://sun1-90.userapi.com/fyBMOQGFv_j9bxEgrYJAODHiKe56x8H0nMUuHA/0eNG3m79q9U.jpg')
							vk.messages.send(user_id=event.user_id,
								message='《Хеллсинг Ultimate》\nОценка 9.26/10\n\nХеллсинг - тайная организация британского правительства, с давних пор сражается с сверхествественными угрозами и держит людей в безопасности от ночных монстров.'
								        '\nНынешний лидер - Интегра Вингейтс Хеллсинг, управляет своей собственной армией для устранения вампиров и гулей, но даже мастерство самых лучших ее солдат, меркнет перед силой вампира, который служит Интегре - Алукарда. Вместе с таинственным '
								        'дворецким Уолтером, Алукард и его новая ученица - Серас Виктория, и солдаты Организации Хеллсинг, должны бороться не только против вампиров, но так же с Святой Инквизицией Ватикана и Миллениумом, таинственной немецкой организацией, '
								        'созданной еще в начале второй мировой войны...\nКровавая смертельная битва между монстрами вот-вот начнется...',
								attachment=photo, random_id=get_random_id())
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Приключения', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Мафия', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Мистика', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Выберите жанр аниме:',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						else:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Приключения', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Мафия', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Мистика', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Фэнтези', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Драмма', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Извини, я не знаю такого жанра', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				# График доллара
				elif idslov[event.user_id] == 'chart':
					if fhg == '1' or fhg == '3':
						if vksms == 'выйти' or vksms == 'отмена':
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
							keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
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
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
						vk.messages.send(user_id=event.user_id, message='Извини, но в данный момент просмотр графика доллара по отношению к рублю сейчас не доступен((', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
				elif idslov[event.user_id][:5] == 'chart':
					if vksms == 'выйти' or vksms == 'отмена':
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
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

								keyboard = VkKeyboard(one_time=True)
								keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
								keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
								vk.messages.send(user_id=event.user_id,message='График доллара с ' + data1 + ' по ' + data2 + ':', random_id=get_random_id(), keyboard=keyboard.get_keyboard(), attachment=photo1)
								idslov[event.user_id] = 'menu'
								os.remove(PATH1 + str(event.user_id) + '.png')
							except Exception as E:
								traceback.print_exc()
								print(E)
								keyboard = VkKeyboard(one_time=True)
								keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
								keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
								vk.messages.send(user_id=event.user_id, message='Ошибка', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
								idslov[event.user_id] = 'menu'
						else:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Сегодня', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Неправильная запись даты. Повторяю: день.месяц.год', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				# Глитч
				elif idslov[event.user_id] == 'glitch':
					keyboard = VkKeyboard(one_time=True)
					keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
					keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
					if out_game(vksms):
						vk.messages.send(user_id=event.user_id, message='Glitch закрыт✅', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						try:
							num = int(event.text)
							vk.messages.send(user_id=event.user_id, message=glitch(num), random_id=get_random_id(), keyboard=keyboard.get_keyboard())
							idslov[event.user_id] = 'menu'
						except:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Введите целочисленное число', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				# Глитч слово
				elif idslov[event.user_id] == 'glitch_word':
					keyboard = VkKeyboard(one_time=True)
					keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
					keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
					vk.messages.send(user_id=event.user_id, message=word_glitch(event.text),random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					idslov[event.user_id] = 'menu'
				# Погода
				elif idslov[event.user_id] == 'weath':
					keyboard = VkKeyboard(one_time=True)
					keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
					keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
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
							print(E)
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							Weather = 'Извините, я не знаю такого города или страны, попробуйте ещё раз'
						vk.messages.send(user_id=event.user_id, message=Weather, random_id=get_random_id(), keyboard=keyboard.get_keyboard())

				# Калькулятор валют
					# С какой валюты
				elif idslov[event.user_id] == 'calc':
					if out_game(vksms):
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
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
						elif vksms.count('украин') > 0 or vksms.count('гривн') > 0 or vksms.count('uah') > 0 or vksms.count('🇺🇦') > 0:
							idslov[event.user_id] = 'calc uah'
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
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
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
						elif vksms.count('украин') > 0 or vksms.count('гривн') > 0 or vksms.count('uah') > 0 or vksms.count('🇺🇦') > 0:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							idslov[event.user_id] = str(idslov[event.user_id]) + '-uah'
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
					keyboard = VkKeyboard(one_time=True)
					keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
					keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
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
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Введи ПРОСТО ЧИСЛО',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				# Яндекс Переводчик
					# С какого языка
				elif idslov[event.user_id] == 'tr1':
					if out_game(vksms):
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
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
						elif vksms.count('украин') > 0 or event.text == '🇺🇦':
							idslov[event.user_id] = 'tr2 uk'
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
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
						vk.messages.send(user_id=event.user_id, message='Переводчик закрыт✅', random_id=get_random_id(),
							keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('🇷🇺', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('🇬🇧', color=VkKeyboardColor.SECONDARY)
						keyboard.add_line()
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
						elif vksms.count('украин') > 0 or event.text == '🇺🇦':
							idslov[event.user_id] = 'tr3 ' + str(idslov[event.user_id])[4:] + '-uk'
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
					keyboard = VkKeyboard(one_time=True)
					keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
					keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
					if vksms == 'выйти' or vksms == 'отмена':
						vk.messages.send(user_id=event.user_id, message='Переводчик закрыт✅', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						try:

							url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
							key = '!КЛЮЧ К ЯНДЕКС API!'
							text = event.text
							lang = idslov[event.user_id][4:]
							r = requests.post(url, data={'key': key, 'text': text, 'lang': lang}).json()
							Translator = str(r["text"])[2:-2]
						except Exception as e:
							Translator = 'Не получилось перевести'
							print(e)
						vk.messages.send(user_id=event.user_id, message=Translator, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
				# Морзе
				elif idslov[event.user_id] == 'morz':
					if vksms == 'выйти' or vksms == 'отмена':
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
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
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
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
							keyboard = VkKeyboard(one_time=True)
							if v_morze1.count('/') > 0:
								keyboard.add_button('Что за палки /?', color=VkKeyboardColor.SECONDARY)
								keyboard.add_line()
							keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
							keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)

							vk.messages.send(user_id=event.user_id, message=v_morze1, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
							if v_morze1.count('_') > 0 and v_morze1.count('.') > 0:
								v_morze2 = v_morze1.replace('_', '—')
								v_morze2 = v_morze2.replace('.', '*')
								vk.messages.send(user_id=event.user_id, message=v_morze2, random_id=get_random_id())
				elif idslov[event.user_id] == 'morz2':
					if out_game(vksms):
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
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
								keyboard = VkKeyboard(one_time=True)
								keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
								vk.messages.send(user_id=event.user_id, message='Просто введи число', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				elif str(idslov[event.user_id])[:6] == 'morz2.':
					if out_game(vksms):
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
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
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
							keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
							vk.messages.send(user_id=event.user_id, message=morslov[event.user_id],
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())

							morslov[event.user_id] = '0'
							idslov[event.user_id] = 'menu'

				# Игры
				elif idslov[event.user_id] == 'play':
					if out_game(vksms):
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
						vk.messages.send(user_id=event.user_id, message='Приходи еще поиграть✅', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						if vksms == '1' or vksms.count('орел и решка') > 0 or vksms.count('орёл и решка') > 0:
							idslov[event.user_id] = 'coin'
							coin = random.randint(0, 1)
							if coin == 0:
								coin = 'Орёл'
							elif coin == 1:
								coin = 'Решка'
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Еще раз', color=VkKeyboardColor.POSITIVE)
							keyboard.add_line()
							keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message=coin + '!\nМожет еще раз?', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms == '2' or vksms.count('отгадай число') > 0:
							chislo = random.randint(1, 100)
							idslov[event.user_id] = 'randint 0.' + str(chislo)
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
							keyboard.add_line()
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Я загадал число от 1 до 100, отгадай его!\nТвой вариант:',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms == '3' or vksms.count('быки и коровы') > 0:
							idslov[event.user_id] = 'bull'
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Правила игры', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Трехзначное', color=VkKeyboardColor.PRIMARY)
							keyboard.add_button('Четырехзначное', color=VkKeyboardColor.PRIMARY)
							keyboard.add_line()
							keyboard.add_button('Пятизначное', color=VkKeyboardColor.PRIMARY)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Хорошо, сыграем в "Быки и коровы". Какое число будешь отгадывать?',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						elif vksms == '4' or vksms.count('виселица') > 0:
							word = rope_word()
							word = word.upper()
							idslov[event.user_id] = 'rope.' + word + ' 0/0-0'
							win_word = ''
							for i in range(len(word)):
								win_word += " _"
							win_word = win_word[1:]
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Правила игры', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
							keyboard.add_line()
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							photo = add_photo_from_computer("Hangman-0.png")
							vk.messages.send(user_id=event.user_id, message= win_word + '\n❤Осталось жизней: 6\n💥Ошибки:',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard(), attachment=photo)
						else:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('1', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('2', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('3', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('4', color=VkKeyboardColor.SECONDARY)
							keyboard.add_line()
							keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Просто напиши номер игры',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				# Орел и решка
				elif idslov[event.user_id] == 'coin':
					if out_game(vksms):
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('1', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('2', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('3', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('4', color=VkKeyboardColor.SECONDARY)
						keyboard.add_line()
						keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Да уж, такая игра может быстро наскучить🔙',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						vk.messages.send(user_id=event.user_id, message=str_games, random_id=get_random_id(),
							keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'play'
					elif (vksms.count('еще') > 0 or vksms.count('ещё') > 0) and vksms.count('раз') > 0:
						idslov[event.user_id] = 'coin'
						coin = random.randint(0, 1)
						if coin == 0:
							coin = 'Орёл'
						elif coin == 1:
							coin = 'Решка'
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Еще раз', color=VkKeyboardColor.POSITIVE)
						keyboard.add_line()
						keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message=coin + '!\nМожет еще раз?',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					else:
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Еще раз', color=VkKeyboardColor.POSITIVE)
						keyboard.add_line()
						keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Извини, я тебя не понял. Повторяю:\nМожет еще раз?',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				# Число от 1 до 100
				elif idslov[event.user_id][:7] == 'randint':
					a = idslov[event.user_id].find('.')
					chislo = idslov[event.user_id][a + 1:]
					motion = idslov[event.user_id][8:a]
					if out_game(vksms):
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('1', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('2', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('3', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('4', color=VkKeyboardColor.SECONDARY)
						keyboard.add_line()
						keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Ладно, еще как нибудь поиграем🔙',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						vk.messages.send(user_id=event.user_id, message=str_games, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'play'
					elif vksms == 'сдаться' or vksms == 'сдаюсь':
						idslov[event.user_id] = 'randint e'
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Еще раз', color=VkKeyboardColor.POSITIVE)
						keyboard.add_line()
						keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Ха-ха! А ты быстро сдался! Всего на ' + str(motion) + ' попытке. \nЧисло было ' + str(chislo) + '\nМожет еще раз?',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif (vksms.count('еще') > 0 or vksms.count('ещё') > 0) and vksms.count('раз') > 0:
						chislo = random.randint(1, 100)
						idslov[event.user_id] = 'randint 0.' + str(chislo)
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Я загадал число от 1 до 100, отгадай его!\nТвой вариант:',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif chislo != 'e':
						try:
							g = int(event.text)
							chislo = int(chislo)
							motion = int(motion)
							if chislo>=1 and chislo<=100:
								if chislo > g:
									motion = int(motion) + 1
									idslov[event.user_id] = 'randint ' + str(motion) + '.' + str(chislo)
									keyboard = VkKeyboard(one_time=True)
									keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
									keyboard.add_line()
									keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
									vk.messages.send(user_id=event.user_id, message='Больше', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
								elif chislo < g:
									motion = int(motion) + 1
									idslov[event.user_id] = 'randint ' + str(motion) + '.' + str(chislo)
									keyboard = VkKeyboard(one_time=True)
									keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
									keyboard.add_line()
									keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
									vk.messages.send(user_id=event.user_id, message='Меньше', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
								elif chislo == g:
									keyboard = VkKeyboard(one_time=True)
									keyboard.add_button('Еще раз', color=VkKeyboardColor.POSITIVE)
									keyboard.add_line()
									keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)

									if (motion >= 5 and motion <= 20) or (motion % 10 == 0 or motion % 10 >= 5):
										pop = ' попыток'
									elif (motion >= 2 and motion <= 4) or (motion % 10 >= 2 and motion % 10 <= 4):
										pop = ' попытки'
									elif motion == 1 or motion % 10 >= 1 and motion > 10:
										pop = ' попытку'
									else:
										pop = ' попыток'
									vk.messages.send(user_id=event.user_id, message='Да, я загадал ' + str(chislo) + '! Ты справился за ' + str(motion) + pop + '\nМожет еще раз?',
									random_id=get_random_id(), keyboard=keyboard.get_keyboard())
							else:
								keyboard = VkKeyboard(one_time=True)
								keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
								keyboard.add_line()
								keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
								vk.messages.send(user_id=event.user_id, message='Напиши число от 1 до 100',
									random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						except:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
							keyboard.add_line()
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Напиши ПРОСТО ЧИСЛО', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				# Быки и коровы меню
				elif idslov[event.user_id] == 'bull':
					if out_game(vksms):
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('1', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('2', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('3', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('4', color=VkKeyboardColor.SECONDARY)
						keyboard.add_line()
						keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Быки и коровы грустно опустили головы🔙', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						vk.messages.send(user_id=event.user_id, message=str_games, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'play'
					elif vksms == 'правила' or vksms == 'правила игры':
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Правила игры', color=VkKeyboardColor.SECONDARY)
						keyboard.add_line()
						keyboard.add_button('Трехзначное', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Четырехзначное', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Пятизначное', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id,
							message='Правила игры "Быки и коровы":\nВ классическом варианте игра рассчитана на двух игроков. '
									'Каждый из игроков задумывает и записывает тайное 4-значное число с неповторяющимися цифрами. '
									'Игрок, который начинает игру по жребию, делает первую попытку отгадать число. '
									'Попытка — это 4-значное число с неповторяющимися цифрами, сообщаемое противнику. '
									'Противник сообщает в ответ, сколько цифр угадано без совпадения с их позициями в тайном числе (то есть количество коров) '
									'и сколько угадано вплоть до позиции в тайном числе (то есть количество быков). Например:\nЗадумано тайное число «3219».\nПопытка: «2310».'
									'\nРезультат: две «коровы» (две цифры: «2» и «3» — угаданы на неверных позициях) и один «бык» (одна цифра «1» угадана вплоть до позиции).'
									'\nПри игре против компьютера игрок вводит комбинации одну за другой, пока не отгадает всю последовательность.\nВАЖНО:'
									'В этой игре числа случайно генерируются так, чтобы цифры внутри не совпадали и число не начиналось на 0',
							random_id=get_random_id()),
						vk.messages.send(user_id=event.user_id,
						message='Прочитал? А теперь выбери какое число ты будешь отгадывать:', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms == 'трехзначное' or vksms == 'трёхзначное':
						r = randcow(3)
						idslov[event.user_id] = 'bull 0.' + r
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Я загадал трехзначное число\nТвой вариант:',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms == 'четырехзначное' or vksms == 'четырёхзначное':
						r = randcow(4)
						idslov[event.user_id] = 'bull 0.' + r
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Я загадал четырехзначное число\nТвой вариант:',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms == 'пятизначное':
						r = randcow(5)
						idslov[event.user_id] = 'bull 0.' + r
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Я загадал пятизначное число\nТвой вариант:',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					else:
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Правила игры', color=VkKeyboardColor.SECONDARY)
						keyboard.add_line()
						keyboard.add_button('Трехзначное', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Четырехзначное', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Пятизначное', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Просто выбери один из вариантов ниже',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				# Быки и коровы игра
				elif idslov[event.user_id][:4] == 'bull':
					a = idslov[event.user_id].find('.')
					chislo = idslov[event.user_id][a + 1:]
					motion = idslov[event.user_id][5:a]
					if out_game(vksms):
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('1', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('2', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('3', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('4', color=VkKeyboardColor.SECONDARY)
						keyboard.add_line()
						keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Быки и коровы грустно опустили головы🔙', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						vk.messages.send(user_id=event.user_id, message=str_games, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'play'
					elif vksms == 'сдаться' or vksms == 'сдаюсь':
						idslov[event.user_id] = 'bull e'
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Еще раз', color=VkKeyboardColor.POSITIVE)
						keyboard.add_line()
						keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(message='Быки и коровы сейчас лопнут от смеха! Ты сдался всего на ' + str(motion) + ' попытке. \nЧисло было ' + str(chislo) + '\nМожет еще раз?',
						user_id=event.user_id, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif (vksms.count('еще') > 0 or vksms.count('ещё') > 0) and vksms.count('раз') > 0:
						idslov[event.user_id] = 'bull'
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Правила игры', color=VkKeyboardColor.SECONDARY)
						keyboard.add_line()
						keyboard.add_button('Трехзначное', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Четырехзначное', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Пятизначное', color=VkKeyboardColor.PRIMARY)
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id,
							message='Ещё раз так ещё раз. Какое число будешь отгадывать?', random_id=get_random_id(),
							keyboard=keyboard.get_keyboard())
					else:
						if chislo != 'e':
							try:
								g = int(event.text)
								chislo = int(chislo)
								motion = int(motion)
								if len(event.text) == len(str(chislo)):
									if repetition(event.text):
										if event.text[0] != '0':
											if chislo != g:
												v = str(chislo)
												a = str(g)
												bulls = 0
												cows = 0
												for i in v:
													if a.count(i) > 0:
														f1 = v.find(i)
														f2 = a.find(i)
														if f1 == f2:
															bulls += 1
														else:
															cows += 1
												motion = int(motion) + 1
												idslov[event.user_id] = 'bull ' + str(motion) + '.' + str(chislo)
												keyboard = VkKeyboard(one_time=True)
												keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
												keyboard.add_line()
												keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
												vk.messages.send(user_id=event.user_id, message='Нет, не угадал!\n🐂Быков: ' + str(bulls) + '\n🐄Коров: ' + str(cows) + '\nТвой вариант:',
												random_id=get_random_id(), keyboard=keyboard.get_keyboard())
											elif chislo == g:
												keyboard = VkKeyboard(one_time=True)
												keyboard.add_button('Еще раз', color=VkKeyboardColor.POSITIVE)
												keyboard.add_line()
												keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)

												if (motion >= 5 and motion <= 20) or (motion % 10 == 0 or motion % 10 >= 5):
													pop = ' попыток'
												elif (motion >= 2 and motion <= 4) or (motion % 10 >= 2 and motion % 10 <= 4):
													pop = ' попытки'
												elif (motion == 1 or motion % 10 >= 1) and motion > 10:
													pop = ' попытку'
												else:
													pop = ' попыток'
												vk.messages.send(user_id=event.user_id, message='Да, я загадал ' + str(chislo) + '! Ты справился за ' + str(motion) + pop + '\nМожет еще раз?',
													random_id=get_random_id(), keyboard=keyboard.get_keyboard())
										else:
											keyboard = VkKeyboard(one_time=True)
											keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
											keyboard.add_line()
											keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
											vk.messages.send(user_id=event.user_id, message='Число не может начинаться на ноль',
												random_id=get_random_id(), keyboard=keyboard.get_keyboard())
									else:
										keyboard = VkKeyboard(one_time=True)
										keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
										keyboard.add_line()
										keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
										vk.messages.send(user_id=event.user_id,
											message='Цифры не должны повторяться', random_id=get_random_id(),
											keyboard=keyboard.get_keyboard())
								else:
									if len(str(chislo)) == 3:
										add = 'ТРЁХЗНАЧНОЕ'
									elif len(str(chislo)) == 4:
										add = 'ЧЕТЫРЁХЗНАЧНОЕ'
									elif len(str(chislo)) == 5:
										add = 'ПЯТИЗНАЧНОЕ'
									else:
										add = 'ТОЧТОЯЗАГАЛЗНАЧНОЕ'
									keyboard = VkKeyboard(one_time=True)
									keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
									keyboard.add_line()
									keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
									vk.messages.send(user_id=event.user_id, message='Повторяю: я загадал ' + add + ' число',
										random_id=get_random_id(), keyboard=keyboard.get_keyboard())
							except:
								keyboard = VkKeyboard(one_time=True)
								keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
								keyboard.add_line()
								keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
								vk.messages.send(user_id=event.user_id, message='Напиши ПРОСТО ЧИСЛО', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				# Виселица
				elif idslov[event.user_id][:4] == 'rope':
					if idslov[event.user_id] == 'rope e':
						orent = 'e'
					else:
						orent = 'a'

						text = idslov[event.user_id]
						a = text.find('.')
						b = text.find(' ')
						c = text.find('/')
						d = text.find('-')
						word = text[a+1:b]
						yes_lett = text[b+1:c]
						no_lett = text[c+1:d]
						motion = int(text[d+1:])
					if out_game(vksms):
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('1', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('2', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('3', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('4', color=VkKeyboardColor.SECONDARY)
						keyboard.add_line()
						keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id, message='Ещё как нибудь поиграем🔙',
							random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						vk.messages.send(user_id=event.user_id, message=str_games, random_id=get_random_id(),
							keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'play'
					elif vksms == 'правила' or vksms == 'правила игры':

						nn = word  # делаем все в формат "И _ Р А" (это переменная mm)
						ll = yes_lett
						mm = ''
						for i in nn:
							if ll.count(i) > 0:
								mm += ' ' + i
							else:
								mm += ' _'
						mm = mm[1:]

						if no_lett == '0':  # узнаём жизни
							lives = 6
							no_lett = ''

						mistakes = ''
						for i in enumerate(no_lett):
							if i[0] == 0:
								mistakes += i[1]
							else:
								mistakes += ', ' + i[1]

						else:
							lives = 6 - len(no_lett)
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Правила игры', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						if lives == 6:  # прикрепляем соответствующую жизне картинку
							photo = add_photo_from_computer("Hangman-0.png")
						elif lives == 5:
							photo = add_photo_from_computer("Hangman-1.png")
						elif lives == 4:
							photo = add_photo_from_computer("Hangman-2.png")
						elif lives == 3:
							photo = add_photo_from_computer("Hangman-3.png")
						elif lives == 2:
							photo = add_photo_from_computer("Hangman-4.png")
						elif lives == 1:
							photo = add_photo_from_computer("Hangman-5.png")
						elif lives == 0:
							photo = add_photo_from_computer("Hangman-6.png")

						if orent !='e':
							vk.messages.send(user_id=event.user_id,
								message='Правила игры "Виселица":\nОдин из игроков загадывает слово — пишет на бумаге первую и последнюю букву слова и отмечает '
										'места для остальных букв, например чертами (существует также вариант, когда изначально все буквы слова неизвестны). Также рисуется виселица с петлёй.'
										'\nСогласно традиции русских лингвистических игр, слово должно быть именем существительным, '
										'нарицательным в именительном падеже единственного числа, либо множественного числа при отсутствии у слова формы единственного числа.'
										'\nВторой игрок предлагает букву, которая может входить в это слово. Если такая буква есть в слове, то первый игрок пишет её '
										'над соответствующими этой букве чертами — столько раз, сколько она встречается в слове. '
										'Если такой буквы нет, то к виселице добавляется круг в петле, изображающий голову. Второй игрок продолжает отгадывать '
										'буквы до тех пор, пока не отгадает всё слово. За каждый неправильный ответ первый игрок добавляет одну часть туловища к виселице '
										'(обычно их 6: голова, туловище, 2 руки и 2 ноги, существует также вариант с 8 частями — добавляются ступни, а также самый длинный вариант, '
										'когда сначала за неотгаданную букву рисуются части самой виселицы).'
										'\nЕсли туловище в виселице нарисовано полностью, то отгадывающий игрок проигрывает, считается повешенным. Если игроку удаётся угадать слово, он выигрывает.',
								random_id=get_random_id())
							vk.messages.send(user_id=event.user_id,
							message='Прочитал? А теперь отгадывай слово:\n' + mm + '\n❤Осталось жизней: ' + str(lives) + '\n💥Ошибки: ' + mistakes,
							random_id=get_random_id(), keyboard=keyboard.get_keyboard(), attachment=photo)
						else:
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Правила игры', color=VkKeyboardColor.SECONDARY)
							keyboard.add_button('Еще раз', color=VkKeyboardColor.POSITIVE)
							keyboard.add_line()
							keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id,
								message='Правила игры "Виселица":\nОдин из игроков загадывает слово — пишет на бумаге первую и последнюю букву слова и отмечает '
										'места для остальных букв, например чертами (существует также вариант, когда изначально все буквы слова неизвестны). Также рисуется виселица с петлёй.'
										'\nСогласно традиции русских лингвистических игр, слово должно быть именем существительным, '
										'нарицательным в именительном падеже единственного числа, либо множественного числа при отсутствии у слова формы единственного числа.'
										'\nВторой игрок предлагает букву, которая может входить в это слово. Если такая буква есть в слове, то первый игрок пишет её '
										'над соответствующими этой букве чертами — столько раз, сколько она встречается в слове. '
										'Если такой буквы нет, то к виселице добавляется круг в петле, изображающий голову. Второй игрок продолжает отгадывать '
										'буквы до тех пор, пока не отгадает всё слово. За каждый неправильный ответ первый игрок добавляет одну часть туловища к виселице '
										'(обычно их 6: голова, туловище, 2 руки и 2 ноги, существует также вариант с 8 частями — добавляются ступни, а также самый длинный вариант, '
										'когда сначала за неотгаданную букву рисуются части самой виселицы).'
										'\nЕсли туловище в виселице нарисовано полностью, то отгадывающий игрок проигрывает, считается повешенным. Если игроку удаётся угадать слово, он выигрывает.',
								random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms == 'сдаться' or vksms == 'сдаюсь':
						idslov[event.user_id] = 'rope e'
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Правила игры', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('Еще раз', color=VkKeyboardColor.POSITIVE)
						keyboard.add_line()
						keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
						vk.messages.send(user_id=event.user_id,
						message='Не такое уж и сложное было слово! Ты сдался всего на ' + str(motion) + ' попытке. \nСлово было ' + word + '\nМожет еще раз?',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif (vksms.count('еще') > 0 or vksms.count('ещё') > 0) and vksms.count('раз') > 0:
						word = rope_word()
						word = word.upper()
						idslov[event.user_id] = 'rope.' + word + ' 0/0-0'
						win_word = ''
						for i in range(len(word)):
							win_word += " _"
						win_word = win_word[1:]
						keyboard = VkKeyboard(one_time=True)
						keyboard.add_button('Правила игры', color=VkKeyboardColor.SECONDARY)
						keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
						keyboard.add_line()
						keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
						photo = add_photo_from_computer("Hangman-0.png")
						vk.messages.send(user_id=event.user_id, message=win_word + '\nОсталось жизней: 6\nОшибки:',
						random_id=get_random_id(), keyboard=keyboard.get_keyboard(), attachment=photo)
					else:
						if orent != 'e':
							if len(event.text) == 1:
								sms = event.text.upper()
								alfavit = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
								if alfavit.count(sms) > 0:
									if no_lett == '0': #узнаём жизни
										lives = 6
										no_lett = ''
									else:
										lives = 6 - len(no_lett)

									if yes_lett.count(sms) > 0 or no_lett.count(sms) > 0: #если говорил букву
										keyboard = VkKeyboard(one_time=True)
										keyboard.add_button('Правила игры', color=VkKeyboardColor.SECONDARY)
										keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
										keyboard.add_line()
										keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
										vk.messages.send(user_id=event.user_id, message= 'Будь внимательнее, ты уже говорил букву "' + sms +'" 😉',
										random_id=get_random_id(), keyboard=keyboard.get_keyboard())
									else:

										if word.count(sms) > 0: #угадал
											yes_lett+=sms
											guess = '✅Угадал!'
										else: #не угадал
											guess = '🚫Не угадал!'
											no_lett+=sms
											lives-=1

										nn = word #делаем все в формат "И _ Р А" (это переменная mm)
										ll = yes_lett
										mm = ''
										for i in nn:
											if ll.count(i) > 0:
												mm += ' ' + i
											else:
												mm += ' _'
										mm = mm[1:]
										g_word = ''
										for i in mm:
											if i != ' ':
												g_word += i
										if lives == 6: #прикрепляем соответствующую жизни картинку
											photo = add_photo_from_computer("Hangman-0.png")
										elif lives == 5:
											photo = add_photo_from_computer("Hangman-1.png")
										elif lives == 4:
											photo = add_photo_from_computer("Hangman-2.png")
										elif lives == 3:
											photo = add_photo_from_computer("Hangman-3.png")
										elif lives == 2:
											photo = add_photo_from_computer("Hangman-4.png")
										elif lives == 1:
											photo = add_photo_from_computer("Hangman-5.png")
										elif lives == 0:
											photo = add_photo_from_computer("Hangman-6.png")
										if lives == 0:
											idslov[event.user_id] = 'rope e'
											keyboard = VkKeyboard(one_time=True)
											keyboard.add_button('Правила игры', color=VkKeyboardColor.SECONDARY)
											keyboard.add_button('Еще раз', color=VkKeyboardColor.POSITIVE)
											keyboard.add_line()
											keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
											vk.messages.send(user_id=event.user_id,
											message='Поражение! Ты проиграл на ' + str(motion) + ' попытке. \nСлово было ' + str(word) + '\nМожет еще раз?',
											random_id=get_random_id(), keyboard=keyboard.get_keyboard())
										elif g_word == word:
											keyboard = VkKeyboard(one_time=True)
											keyboard.add_button('Еще раз', color=VkKeyboardColor.POSITIVE)
											keyboard.add_line()
											keyboard.add_button('Выйти', color=VkKeyboardColor.NEGATIVE)
											if (motion >= 5 and motion <= 20) or (motion % 10 == 0 or motion % 10 >= 5):
												pop = ' попыток'
											elif (motion >= 2 and motion <= 4) or (motion % 10 >= 2 and motion % 10 <= 4):
												pop = ' попытки'
											elif (motion == 1 or motion % 10 >= 1) and motion > 10:
												pop = ' попытку'
											else:
												pop = ' попыток'
											vk.messages.send(user_id=event.user_id,
											message='Победа! Ты справился за ' + str(motion) + pop + '. \nСлово было ' + str(word) + '\nМожет еще раз?',
											random_id=get_random_id(), keyboard=keyboard.get_keyboard())
										else:
											keyboard = VkKeyboard(one_time=True)
											keyboard.add_button('Правила игры', color=VkKeyboardColor.SECONDARY)
											keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
											keyboard.add_line()
											keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
											mistakes = ''
											for i in enumerate(no_lett):
												if i[0] == 0:
													mistakes+=i[1]
												else:
													mistakes+= ', ' + i[1]
											vk.messages.send(user_id=event.user_id, message=guess + '\n' + mm + '\n❤Осталось жизней: ' + str(lives) + '\n💥Ошибки: ' + mistakes,
											random_id=get_random_id(), keyboard=keyboard.get_keyboard(), attachment=photo)
											if no_lett == '':
												no_lett = '0'
											if yes_lett == '':
												yes_lett = '0'
											motion+=1
											idslov[event.user_id] = 'rope.' + word + ' ' + yes_lett + '/' + no_lett + '-' + str(motion)
								else:
									keyboard = VkKeyboard(one_time=True)
									keyboard.add_button('Правила игры', color=VkKeyboardColor.SECONDARY)
									keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
									keyboard.add_line()
									keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
									vk.messages.send(user_id=event.user_id, message='Напиши БУКВУ',
										random_id=get_random_id(), keyboard=keyboard.get_keyboard())
							else:
								keyboard = VkKeyboard(one_time=True)
								keyboard.add_button('Правила игры', color=VkKeyboardColor.SECONDARY)
								keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
								keyboard.add_line()
								keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
								vk.messages.send(user_id=event.user_id, message= 'Напиши ОДНУ букву', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
	except Exception as E:
		print('Ошибка: ' + str(E))
		traceback.print_exc()
		print('Перезапуск...')
		time.sleep(1)