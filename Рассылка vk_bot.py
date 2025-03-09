# coding=utf-8
import requests
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

vk_session = vk_api.VkApi(token='a275ef4cebed4bcb40c997fe869363e0b595d6e26170359606313ce8cdd53b56ebac4a52e175215f17895')
vk = vk_session.get_api()
f = '370149438 572875785 569626801 356556313 44195316 198987764 465097169 547903893 323750809 351063001 452479083 474543841 521654133 541926694 396642267 346778589 372199459 444109392 291732154 461465891 122663436 233279934 383961196 306022377 519029533 202449768 449098041 441399727 535655584 328907879 237653092 381467372 591353957 304096184 532876437 568113044 192715041 328905922 537412593'
b = f.split()
idlist = []
for i in b:
	idlist.append(int(i))
print(idlist)
keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Что обновили?', color=VkKeyboardColor.DEFAULT)
keyboard.add_line()
keyboard.add_button('Играть', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('Что ты умеешь?', color=VkKeyboardColor.POSITIVE)
h = 0
for id in idlist:
	try:
		vk.messages.send(user_id=id, message='💫Приветик. Это было немного сложновато, но я сменил платформу, '
		                                     'на которой работает этот бот. Теперь он не должен вылетать и по задумке '
		                                     'будет работать ВЕЧНО (ну, или по-крайней мере будет вылетать не так '
		                                     'часто). Надеюсь, вам нравится этот бот так же, как и мне и все мои '
		                                     'старания не идут зря. Во время разработки этого бота я получил много '
		                                     'опыта в работе с VK Api и не собираюсь останавливаться. Со временем он '
		                                     'будет развиваться, сейчас была просто некоторая передышка. Не забывайте '
		                                     'рассказывать о нем друзьям, это очень развивает паблик и о боте узнает '
		                                     'больше людей. Спасибо, что вы со мной.', random_id=get_random_id(),
			keyboard=keyboard.get_keyboard())
		print('✔ ' + str(id))
		h+=1
	except:
		print('❌ ' + str(id))
print('Расслыка готова (' + str(h) + ' человек)')