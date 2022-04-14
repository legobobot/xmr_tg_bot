from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# default_key-----------------------------------------------------------------
more = KeyboardButton("🔞Nudes🔞")
menu = KeyboardButton("↩️ Главное меню")
morebtn = ReplyKeyboardMarkup(resize_keyboard=True).row(more, menu)
# admin_menu--------------------------------------------------------------------
Upload_file = KeyboardButton("Добавить")
del_file = KeyboardButton("Удалить")
back_to_one = KeyboardButton("Назад")
admin_menu = (ReplyKeyboardMarkup(resize_keyboard=True).row(
    Upload_file, del_file)).row(back_to_one, menu)
