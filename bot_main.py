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
	first_name = State()
	surname = State()
	# отчество
	patronymic = State()

@dp.message_handler(commands="start")
async def get_info(message: types.Message):
	await message.reply("Hi!\nI am FESTU schedule bot")
	await message.answer("Введите номер вашей группы")
	#setting user group
	await UserState.group.set()

@dp.message_handler(state=UserState.group)
async def get_usergroup(message: types.Message, state: FSMContext):
	await state.update_data(group=message.text)
	await message.answer("Отлично! Теперь введите ваше имя")
	await UserState.first_name.set()

@dp.message_handler(state=UserState.first_name)
async def get_username(message: types.Message, state: FSMContext):
	await state.update_data(first_name=message.text)
	await message.answer("Отлично! Теперь введите вашу фамилию")
	await UserState.surname.set()

@dp.message_handler(state=UserState.surname)
async def get_usersurname(message: types.Message, state: FSMContext):
	await state.update_data(surname=message.text)
	await message.answer("Отлично! Теперь введите ваше отчество")
	await UserState.patronymic.set()

@dp.message_handler(state=UserState.patronymic)
async def get_userpatronymic(message: types.Message, state: FSMContext):
	await state.update_data(patronymic=message.text)
	data = await state.get_data()
	line = "Приветствуем вас, {0} {1} {2}". \
	format(data['surname'], data['first_name'],
		data['patronymic'])
	await message.answer(line)
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
	shedule_button = types.KeyboardButton(text="/расписание")
	rating_button = types.KeyboardButton(text="/рейтинг")

	keyboard.add(shedule_button, rating_button)

	await message.answer("""Возможности:
		\n/расписание - получить расписание
		\n/рейтинг - получить рейтинг""", 
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

@dp.message_handler(commands=['рейтинг'])
async def send_rating(message: types.Message):
	"""
	This handler will be called when user sends
	"рейтинг"
	"""
	await message.answer("рейтинг")


@dp.message_handler(commands=["сегодня", "завтра"])
async def send_timetable_for_today(message: types.Message):
	if message.text == "/сегодня":
		await message.answer("расписание на сегодня")
	elif message.text == "/завтра":
		await message.answer("расписание на завтра")



@dp.message_handler()
async def not_understand(message:types.Message):
	await message.answer("Прости, не понимаю тебя")


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)