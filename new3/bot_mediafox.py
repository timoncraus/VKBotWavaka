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
token1 = 'vk1.a.DSnVdrc6a0TMsikg4VnaopBHK7kaGSdDag8aIMZIN9vLmrdnIqLqzmrfi6oXhWZ4RZUpLuCn6w136OhDg5SYq2-wjvpdK4wfguF28aGyN2PZY5rH6Y1Mx67azu5m_9PhEeL4P-7w_kBYn4ibCx1PHxNH-A7HBNfh1RXkBDr_RMinO0Y6042cyHeOQd4QlxPTSENF9AVnCyazBh8ilVsvpg'
group_id = '236394828'
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
str_skills = 'Я развлекательный бот. Авторы: Горшков Тимофей, Мендыгалиев Данияр, Барсуков Максим (2026 г.). Вот, что я умею:' \
			 '\n🎦 Напиши "что посмотреть" или "что глянуть" и т.д., чтобы войти в меню просмотра нашей подборки лучших сериалов и фильмов' \
			 '\n⭐ Напиши "игры", "играть", "давай поиграем", "поигрунькать", и т.д., чтобы открыть список игр' \
			 '\n⭐ Напиши "факты", "интересный факт", "расскажи факт" и т.д., чтобы узнать случайный факт'\
			 '\n⭐ Напиши "ландыши", "розы", "ромашка" и т.д., чтобы получить фото тех или иных цветов (чтобы узнать, какие цветы доступны, напиши "цветы")' \
			 '\n⭐ Напиши "глитч" или "glitch", чтобы получить случайный набор символов' \
			 '\n⭐ Напиши "глитч слова" или "glitch слово" и т.д., чтобы зашифровать свое сообщение случайным набором символов' \
			 '\n⭐ Напиши "стабильность", чтобы узнать, сколько бот отправил сообщений, начиная с 4.03.26' \
             '\n🔆 А вообще можешь просто со мной поболтать😄'
str_data_v = 'Версия ' + version + '\nДаты других версий: ' \
								   '\n"test_group", "bot_tima" - 1.0 (17.02.2020)' \
								   '\n"Wavaka" - 2.0 (23.02.20)' \
								   '\n"Wavaka" - 2.1 (8.03.20)' \
								   '\n"Wavaka" - 2.2 (27.03.20)' \
								   '\n"Wavaka" - 2.3 (22.04.20)'
str_flowers = '🌺Вот, какие цветы доступны:' \
			  '\nРозы, гвоздики, тюльпаны, ромашки, ландыши, подсолнух, нарциссы, мимозы, герберы, орхидеи, ирисы, сирени, гардении, жасмины, магнолии, гиацинты, гладиолусы'

# Функции:
def get_main_menu_keyboard():
	keyboard = VkKeyboard(one_time=True)
	keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
	keyboard.add_button('О программе', color=VkKeyboardColor.POSITIVE)
	keyboard.add_line()
	keyboard.add_button('Что посмотреть', color=VkKeyboardColor.SECONDARY)
	keyboard.add_line()
	keyboard.add_button('Факты', color=VkKeyboardColor.SECONDARY)
	keyboard.add_button('Ромашка', color=VkKeyboardColor.SECONDARY)
	keyboard.add_line()
	keyboard.add_button('Глитч', color=VkKeyboardColor.SECONDARY)
	keyboard.add_button('Глитч слова', color=VkKeyboardColor.SECONDARY)
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
						vk.messages.send(user_id=event.user_id, message='Я русскоязычный бот ВКонтакте под названием MediaFox. Сделан студентами ОГУ на языке программирования Python через Vk API\nВерсия ' + version + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
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
						vk.messages.send(user_id=event.user_id, message='Начиная с 4.03.26 обработано ' + str(stab) + ' сообщений🚀' + sub,
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
					elif vksms.count('поделиться') > 0 or (vksms.count('рассказать') > 0 and vksms.count('друзьям') > 0):
						vk.messages.send(user_id=event.user_id, message='Если хочешь рассказать обо мне другим, используй эту ссылку:\n@club236394828' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('рассылк') > 0:
						vk.messages.send(user_id=event.user_id, message='Ничего не слышу😙🎶' + sub, random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('реклам') > 0:
						vk.messages.send(user_id=event.user_id, message='По поводу рекламы писать Тимофею в лс:\n@tima.gorshkov', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('вау') > 0 or (vksms.count('ух') > 0 and vksms.count('ты') > 0) or (vksms.count('в') > 0 and vksms.count('шоке') > 0) or vksms.count('обалдеть') > 0 or vksms.count('офигеть') > 0 or vksms.count('охренеть') > 0:
						vk.messages.send(user_id=event.user_id, message='Я сам в шоке😯', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					elif vksms.count('админ') > 0 or vksms.count('главный') > 0 or vksms.count('главного') > 0:
						vk.messages.send(user_id=event.user_id, message='Админ:\n@tima.gorshkov', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
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
				# Что Посмотреть
				elif idslov[event.user_id] == 'l_menu':
					if out_game(vksms):
						keyboard = get_main_menu_keyboard()
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
				
				# Глитч
				elif idslov[event.user_id] == 'glitch':
					keyboard = get_main_menu_keyboard()
					if out_game(vksms):
						vk.messages.send(user_id=event.user_id, message='Glitch закрыт✅', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
						idslov[event.user_id] = 'menu'
					else:
						try:
							num = int(event.text)
							vk.messages.send(user_id=event.user_id, message=glitch(num), random_id=get_random_id(), keyboard=keyboard.get_keyboard())
							idslov[event.user_id] = 'menu'
						except:
							traceback.print_exc()
							keyboard = VkKeyboard(one_time=True)
							keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
							vk.messages.send(user_id=event.user_id, message='Введите целочисленное число', random_id=get_random_id(), keyboard=keyboard.get_keyboard())
				# Глитч слово
				elif idslov[event.user_id] == 'glitch_word':
					keyboard = get_main_menu_keyboard()
					vk.messages.send(user_id=event.user_id, message=word_glitch(event.text),random_id=get_random_id(), keyboard=keyboard.get_keyboard())
					idslov[event.user_id] = 'menu'
				# Игры
				elif idslov[event.user_id] == 'play':
					if out_game(vksms):
						keyboard = get_main_menu_keyboard()
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
							traceback.print_exc()
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
								traceback.print_exc()
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