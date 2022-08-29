from aiogram import Bot, Dispatcher

from config import Config

token = Config('tg_token')

bot = Bot(token=token)
dp = Dispatcher(bot) if bot and token else False
