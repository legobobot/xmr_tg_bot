from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

QIWI_TOKEN = "YOUR QIWI TOKEN"
API_TOKEN = "YOUR BOT TOKEN"


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
