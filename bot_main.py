# library for logging activities
import logging
import aiogram
from aiogram import Bot, Dispatcher, executor, types

# memory for fsm
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# states for getting info grom user
from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram.dispatcher import FSMContext
from settings import API_TOKEN, rating_url

import rating

import search

#from schedule_rating import main

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
# storage inside operative memory
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

user_dict = {
	"username": None,
	"group": None,
}

class UserState(StatesGroup):
	group = State()
	username = State()

@dp.message_handler(commands="start")
async def get_info(message: types.Message):
	text = """Привет, я бот ДВГУПС.\
	\nМеня зовут Лизи!\
	\nЯ создана для того, чтобы помочь тебе в суровой студенческой жизни.\
	\nНо для начала, давай познакомимся...
	\nКак тебя зовут? (ФИО)"""
	await message.answer(text)
	#setting user group
	await UserState.username.set()

@dp.message_handler(state=UserState.username)
async def get_username(message: types.Message, state: FSMContext):
	name = message.text.split()
	if len(name) != 3:
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
			await message.answer("Номер группы изменён.")
			await change_info(message)


@dp.message_handler(commands=["help", "назад"])
async def send_welcome(message: types.Message):
	"""
	This handler will be called when user sends 
	"/start" and "/help"
	"""
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
		one_time_keyboard=True)
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
	if message.text == "Сегодня":
		# send photo
		await message.answer("расписание на сегодня")
	elif message.text == "Завтра":
		# send_photo
		await message.answer("расписание на завтра")

@dp.message_handler(commands=["успеваемость"])
async def send_rating(message: types.Message):
	"""
	This handler will be called when user sends
	"успеваемость"
	"""
	data = search.user_pull(id=message.from_user.id)

	filename = rating.rating(username=user_dict["username"],
		groupname=user_dict["group"])

	with open(filename, 'rb') as file:
		await message.answer_photo(file)
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
	line = """Тебя зовут {0},\
	\nты из группы {1}.\
	\nИли я в чём-то ошиблась?"""\
	.format()
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	change_name = types.KeyboardButton(text="изменить ФИО")
	change_group = types.KeyboardButton(text="изменить группу")
	back_button = types.KeyboardButton(text="всё верно")

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
	\n\nВлад - https://vk.com/id544196085"""

	await message.answer(info_line, reply_markup=markup)
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