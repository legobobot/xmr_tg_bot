from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

QIWI_TOKEN = "YOUR QIWI TOKEN"
API_TOKEN = "YOUR BOT TOKEN"
ADMIN_ID = "YOUR ADMIN_ID"  # without -> ""


DataBase = "Files.db"

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
