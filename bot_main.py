# library for logging activities
import logging

from aiogram import Bot, Dispatcher, executor, types

# memory for fsm
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# states for getting info grom user
from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram.dispatcher import FSMContext
from settings import API_TOKEN

#from schedule_rating import main

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
# storage inside operative memory
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class UserState(StatesGroup):
	group = State()
	username = State()

@dp.message_handler(commands="start")
async def get_info(message: types.Message):
	await message.reply("Hi!\nI am FESTU schedule bot")
	await message.answer("Введите номер вашей группы")
	#setting user group
	await UserState.group.set()

@dp.message_handler(state=UserState.group)
async def get_usergroup(message: types.Message, state: FSMContext):
	await state.update_data(group=message.text)
	await message.answer("Отлично! Теперь введите ваше ФИО")
	await UserState.username.set()

@dp.message_handler(state=UserState.username)
async def get_username(message: types.Message, state: FSMContext):
	name = message.text.split()
	if len(name) != 3:
		await message.answer("Вы ввели имя некорректно, попробуйте ещё раз")
		await UserState.username.set()
	else:
		await state.update_data(username=name)
		data = await state.get_data()
		line = "Приветствуем вас, {0} {1} {2}". \
		format(name[0], name[1], name[2])
		await message.answer(line)
		await state.finish()

		await message.answer("Отлично! Вся необходимая информация заполнена")
		await send_welcome(message)

@dp.message_handler(commands=["help", "назад"])
async def send_welcome(message: types.Message):
	"""
	This handler will be called when user sends 
	"/start" and "/help"
	"""
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
		one_time_keyboard=True)
	shedule_button = types.KeyboardButton(text="расписание")
	rating_button = types.KeyboardButton(text="успеваемость")

	keyboard.add(shedule_button, rating_button)

	await message.answer("""Возможности:
		\nрасписание - получить расписание
		\nуспеваемость - получить успеваемость""", 
		reply_markup=keyboard)

@dp.message_handler(commands=["расписание"])
async def send_shedule(message: types.Message):
	"""
	This handler will be called when user asks
	info about shedule by pushing button "/расписание" 
	"""
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
		)
	today_button = types.KeyboardButton(text="/сегодня")
	tommorow_button = types.KeyboardButton(text="/завтра")
	back_button = types.KeyboardButton(text='/назад')

	markup.row(today_button, tommorow_button)
	markup.add(back_button)
	await message.reply("На какой вам день?", 
		reply_markup=markup)

@dp.message_handler(commands=["успеваемость"])
async def send_rating(message: types.Message):
	"""
	This handler will be called when user sends
	"рейтинг"
	"""
	await message.answer("успеваемость")


@dp.message_handler(commands=["сегодня", "завтра"])
async def send_timetable_for(message: types.Message):
	if message.text == "/сегодня":
		await message.answer("расписание на сегодня")
	elif message.text == "/завтра":
		await message.answer("расписание на завтра")



@dp.message_handler()
async def not_understand(message:types.Message):
	row = message.text.strip().lower()
	if "расписание" in row:
		await send_shedule(message)
	elif "успеваемость" in row:
		await send_rating(message)
	else:
		await message.answer("Прости, не понимаю тебя")


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)