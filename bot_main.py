# library for logging activities
import logging
from aiogram import Bot, Dispatcher, executor, types

# memory for fsm
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# states for getting info grom user
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram.dispatcher import FSMContext
from settings import API_TOKEN

from timetable import process

from rating_with_req import info_rating

import search
import re
#from schedule_rating import main

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
# storage inside operative memory
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

user_dict = {
	"username": None,
	"group": None,
}

class UserState(StatesGroup):
	group = State()
	username = State()

@dp.message_handler(commands="start")
async def get_info(message: types.Message):
	try:
		search.user_pull(id=message.from_user.id)
	except IndexError:
		# если человек впервые
		text = """Привет, я бот ДВГУПС.\
		\nМеня зовут Лизи!\
		\nЯ создана для того, чтобы помочь тебе в суровой студенческой жизни.\
		\nНо для начала, давай познакомимся...
		\nКак тебя зовут? (ФИО)"""
		await message.answer(text)
		#setting user group
		await UserState.username.set()
	else:
		# если был до этого
		await change_info(message)

@dp.message_handler(state=UserState.username)
async def get_username(message: types.Message, state: FSMContext):
	name = message.text.split()
	if len(name) != 3 or any(re.search('\d', one) for one in name):
		await message.answer("Вы ввели имя некорректно, попробуйте ещё раз.")
		await UserState.username.set()
	else:
		our_info = ' '.join([i.capitalize() for i in message.text.split()])
		try:
			# узнаём, пользовался ли пользователь ботом прежде
			search.user_pull(id=message.from_user.id)
		except IndexError:
			# значит user впервые, нужно продолжить сбор данных
			await state.update_data(username=our_info)
			text = "Приятно познакомиться, {}!\
			\nА теперь, позволь узнать мне... Из какой ты группы?".format(our_info.split()[1])
			await message.answer(text)
			await UserState.group.set()
		else:
			# если пользователь существует,
			# нужно будет изменить имя о нём
			search.user_name_ch(id=message.from_user.id,
                                newname=our_info)
			await state.finish()
			await message.answer("Имя изменено.")
			await change_info(message)


@dp.message_handler(state=UserState.group)
async def get_usergroup(message: types.Message, state: FSMContext):
	try:
		# проверка на указание нормальной группы
		group_line = message.text.upper()
		info_group_inst = search.group_parse(group_line)
	except IndexError:
		info_line = "Прости, такую группу я не знаю.\
		\nПопробуй ещё раз ввести свою группу."
		await message.answer(info_line)
		await UserState.group.set()
	else:
		# если ввели нормальную группу
		try:
			# впервые ли пользователь определяется здесь
			search.user_pull(message.from_user.id)
		except IndexError:
			# если впервые
			await state.update_data(group=group_line)
			data_from_state = await state.get_data()
			search.user_add(id=message.from_user.id,
                            id_group=info_group_inst[0],
                            id_fac=info_group_inst[1],
                            fullname=data_from_state['username'])
			await state.finish()

			await message.answer("Вау, отлично!")
			line = "Сейчас я расскажу тебе немного о себе.\
			\n\nЯ могу выполнять несколько команд:\
			\n\nРасписание - позволит узнать расписание на сегодняшний и завтрашний день\
			\n\nУспеваемость - даст возможность увидеть свою успеваемость по всем предметам.\
			\n\nНастройки - тут ты сможешь изменить номер своей\
			группы или ФИО, в случае некорректного ввода.\
			Или прочитать о тех, кто меня создал:)"
			msg = await message.answer(line)
			await bot.pin_chat_message(message.from_user.id, msg.message_id)
			await send_welcome(message)
		else:
			# если хочет изменить группу
			search.user_group_ch(id=message.from_user.id,
                                 newgroup_id=info_group_inst[0])
			await state.finish()
			await message.answer("Номер группы изменён.")
			await change_info(message)


@dp.message_handler(commands=["help", "назад"])
async def send_welcome(message: types.Message):
	"""
	This handler will be called when user sends 
	"/start" and "/help"
	"""
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	shedule_button = types.KeyboardButton(text="Расписание")
	rating_button = types.KeyboardButton(text="Успеваемость")

	settings_button = types.KeyboardButton(text="Настройки")
	keyboard.row(shedule_button, rating_button)
	keyboard.add(settings_button)
	msg_text = message.text.lower()
	if ("назад" in msg_text) or ("успеваемость" in msg_text) or \
	("измени" in msg_text) or ("всё верно"in msg_text) or ("о разработчиках" in msg_text):
		line = "Чем помочь?"
	else:
		line = "С чего начнём?"

	await message.answer(line, reply_markup=keyboard)

@dp.message_handler(commands=["расписание"])
async def send_shedule(message: types.Message):
	"""
	This handler will be called when user asks
	info about shedule by pushing button "/расписание" 
	"""
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	today_button = types.KeyboardButton(text="Сегодня")
	tommorow_button = types.KeyboardButton(text="Завтра")
	back_button = types.KeyboardButton(text='Назад')

	markup.row(today_button, tommorow_button)
	markup.add(back_button)
	await message.reply("На какой день ты хочешь узнать расписание?", 
		reply_markup=markup)

@dp.message_handler(commands=["сегодня", "завтра"])
async def send_timetable_for(message: types.Message):
	group_info_user = str(search.user_pull(message.from_user.id)[1])

	if message.text == "Сегодня":
		await message.answer("Расписание на сегодня: \n")
		info = process(group=group_info_user, agreement="С")
	elif message.text == "Завтра":
		await message.answer("Расписание на завтра: \n")
		info = process(group=group_info_user, agreement="З")
	if info.keys():
		msg = ""
		for key in info.keys():
			msg += key + ": " + "\n" + info[key][0] + " " + "\n" +info[key][-1] + "\n\n"
		if msg:
			await message.answer(msg)
	else:
		if message.text == "Сегодня":
			await message.answer("Сегодня нет занятий :)")
		elif message.text == "Завтра":
			await message.answer("Завтра нет занятий :)")

@dp.message_handler(commands=["успеваемость"])
async def send_rating(message: types.Message):
	"""
	This handler will be called when user sends
	"успеваемость"
	"""
	data = search.user_pull(id=message.from_user.id)
	group_line = search.names_parse(data[1])
	fullname = data[-1]
	try:
		results = info_rating(username=fullname,
			group=group_line)
		if results:
			msg = "Успеваемость указана в формате 'Твоя/План':\n\n"
			current_res = ""
			for result in results:
				tmp = result[2]
				if tmp == "-":
					tmp = 0
				current_res += "{}: {}/{}\n\n".format(result[0], tmp, result[1])
			if current_res:
				await message.answer(msg + current_res)
			else:
				raise FileNotFoundError
		else:
			await message.answer("Твоего имени нет с списке группы(")
	except FileNotFoundError:
		await message.answer("Для пользователя с таким именем успеваемость не найдена.\
			\nПроверь свои данные.")
		await change_info(message)
	else:
		await send_welcome(message)

@dp.message_handler(commands=["настройки"])
async def send_settings(message: types.Message):
	"""
	This handler will be called when user sends
	"настройки" or "/настройки"
	"""
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	change_userinfo = types.KeyboardButton(text="Профиль")
	about_developers = types.KeyboardButton(text="О разработчиках")
	back_button = types.KeyboardButton(text="Назад")

	markup.row(change_userinfo, about_developers)
	markup.add(back_button)

	await message.answer("Что ты хочешь?", reply_markup=markup)

@dp.message_handler(commands=['профиль'])
async def change_info(message: types.Message):
	"""
	This handler will ...
	"""
	user = search.user_pull(id=message.from_user.id)
	group_line = search.names_parse(group_id=user[1])

	line = """Тебя зовут {0},\
	\nты из группы {1}.\
	\nИли я в чём-то ошиблась?"""\
	.format(user[-1], group_line)
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	change_name = types.KeyboardButton(text="Изменить ФИО")
	change_group = types.KeyboardButton(text="Изменить группу")
	back_button = types.KeyboardButton(text="Всё верно")

	markup.row(change_name, change_group)
	markup.add(back_button)

	await message.answer(line, reply_markup=markup)

@dp.message_handler(commands=["изменить_фио"])
async def change_username(message: types.Message):
	"""
	This handler will ...
	"""
	line = "Ой, похоже, я неверно записала твоё имя.\
	\n\nВведи своё фамилию, имя, отчество."

	await message.answer(line)
	await UserState.username.set()

@dp.message_handler(commands=["изменить_группу"])
async def change_group(message: types.Message):
	"""
	This handler will ...
	"""
	line = "Ой, видимо, я что-то перепутала, давай исправим.\
	\n\nВведи номер своей группы."

	await message.answer(line)
	await UserState.group.set()

@dp.message_handler(commands=["разработчики"])
async def about_devs(message: types.Message):
	"""
	This handler will send info about us
	"""
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

	info_line = """\
	Ух ты! Ты решил узнать о тех кто меня создал?\
	\nТогда слушай:
	\n\nФируз - https://vk.com/middledev
	\n\nДаня - https://vk.com/stulevtoday
	\n\nВлад - https://vk.com/id544196085
	\n\nЛёва - https://vk.com/l_slonc"""

	await message.answer(info_line, reply_markup=markup, disable_web_page_preview=True)
	await send_welcome(message)

@dp.message_handler()
async def not_understand(message:types.Message):
	row = message.text.strip().lower()
	help_words = ['help', 'помоги', "помогите"]
	if "расписание" in row:
		await send_shedule(message)
	elif ("сегодня" in row) or ("завтра" in row):
		await send_timetable_for(message)
	elif "успеваемость" in row:
		await send_rating(message)
	elif "настройки" in row:
		await send_settings(message)
	elif "профиль" in row:
		await change_info(message)
	elif "изменить фио" in row:
		await change_username(message)
	elif "изменить группу" in row:
		await change_group(message)
	elif "всё верно" in row:
		await send_welcome(message)
	elif ("назад" in row) or (any([(word in row) for word in help_words])):
		await send_welcome(message)
	elif "о разработчиках" in row:
		await about_devs(message)
	else:
		await message.answer("Прости, не понимаю тебя")


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)