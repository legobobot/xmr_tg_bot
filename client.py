from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = "5223501086:AAGrVFoF2xkC0UvES0royfnjBLHlIm0VQ4o"
QIWI_TOKEN = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6Imx6Mjhzcy0wMCIsInVzZXJfaWQiOiI3OTAyNjM2NDU0NyIsInNlY3JldCI6ImIxNjZiODQzNjljNjY1NDQzYzU3Mzg2ZjQxYmE2OTc1NDgxMzk2ZDcxODFmYjYxNGQzMDI0YmVjNjNhZDVkMDMifX0="
ADMIN_ID = 349170112

DataBase = "Files.db"

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
