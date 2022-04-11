from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
from Db import Database
from sqlite_db import main_data as mDATA

data = Database()
# --------Categories---------
categories = InlineKeyboardMarkup(row_width=1)

Girl = InlineKeyboardMarkup(row_width=2)
back = InlineKeyboardButton(
    text="Назад", callback_data="category", row_width=1)


def getKey():
    keys = data.get_keyboard()
    for row in keys:
        try:
            temp = InlineKeyboardButton(
                text=row[0], callback_data=row[0])
            categories.insert(temp)
        except:
            print("Error in import inline-keyboard")
        finally:
            print("keyboard " + row[0] + " added")


def getNewKey():
    categories = InlineKeyboardMarkup(row_width=1)
    keys = data.get_keyboard()
    for row in keys:
        try:
            temp = InlineKeyboardButton(
                text=row[0], callback_data=row[0])
            categories.insert(temp)
        except:
            print("Error in import inline-keyboard")
        finally:
            print("keyboard " + row[0] + " added")
    return categories
# -----------------------------------------


def get_girls_key(title):
    Girl = InlineKeyboardMarkup(row_width=2)
    girls = mDATA.GET_GIRLS_INLINE_KEY(title)
    for i in girls:
        temp = InlineKeyboardButton(
            text=(i[0]), callback_data=i[0])
        Girl.add(temp)
    Girl.row(back)
    return Girl


# ----------Обычные клавиши---------------
help = KeyboardButton("Помощь")
inline = KeyboardButton("Категории")
Inline_key = ReplyKeyboardMarkup(resize_keyboard=True).add(inline, help)
# ----------admin------------------------
add_file = KeyboardButton("Добавить файл")
del_file = KeyboardButton("Удалить файл")
add_cat = KeyboardButton("Добавить категорию")
del_cat = KeyboardButton("Удалить категорию")
Admin_back = KeyboardButton("Назад в главное меню")
admin = ((ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(
    add_file, del_file)).row(add_cat, del_cat)).add(Admin_back)
# ------------------buy--------------------
buybtn = InlineKeyboardMarkup(row_width=3).row(InlineKeyboardButton(
    text="Назад", callback_data="Back"), InlineKeyboardButton(text="КУПИТЬ", callback_data="buy_arr"))
# -----------------help---------------------
errorbtn = KeyboardButton("Связь с поддержкой")
review = KeyboardButton("Отзыв")
help = (ReplyKeyboardMarkup(resize_keyboard=True).row(
    errorbtn, review)).add(Admin_back)

getKey()
