# library for logging activities
import logging

from aiogram import Bot, Dispatcher, executor, types

from settings import API_TOKEN

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
	"""
	This handler will be called when user sends 
	"/start" and "/help"
	"""
	# keyboard
	# resize_keyboard - fits keyboard buttons
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
		one_time_keyboard=True)
	shedule_button = types.KeyboardButton(text="/Расписание")
	rating_button = types.KeyboardButton(text="/Рейтинг")

	keyboard.add(shedule_button, rating_button)

	await message.reply("Hi!\nI am FESTU shedule bot", 
		reply_markup=keyboard)

@dp.message_handler()
async def echo(message:types.Message):
	await message.answer("Прости, не понимаю тебя")


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)