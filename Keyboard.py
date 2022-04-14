from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
from sqlite_db import main_data as data
# --------Categories---------
categories = InlineKeyboardMarkup(row_width=1)
Girl = InlineKeyboardMarkup(row_width=2)
back = InlineKeyboardButton(
    text="Назад", callback_data="category", row_width=1)
# ----------Обычные клавиши---------------
help = KeyboardButton("✅ Поддержка ✅")
inline = KeyboardButton("🛒 Товар")
preview_send = KeyboardButton("🆓 FREE 🆓")
Inline_key = (ReplyKeyboardMarkup(resize_keyboard=True).row(
    inline, preview_send)).add(help)
# ----------admin------------------------
add_file = KeyboardButton("Добавить файл")
del_file = KeyboardButton("Удалить файл")
add_cat = KeyboardButton("Добавить категорию")
del_cat = KeyboardButton("Удалить категорию")
test_photo = KeyboardButton("Редактировать превью фотографии")
Admin_back = KeyboardButton("Назад в главное меню")
admin = (((ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(
    add_file, del_file)).row(add_cat, del_cat)).add(test_photo)).add(Admin_back)
# ------------------buy--------------------
buybtn = InlineKeyboardMarkup(row_width=3).row(InlineKeyboardButton(
    text="Назад", callback_data="Back"), InlineKeyboardButton(text="КУПИТЬ", callback_data="buy_arr"))
# -----------------help---------------------
errorbtn = KeyboardButton("📞 Связь с поддержкой")
review = KeyboardButton("📝 Оставить отзыв")
help = (ReplyKeyboardMarkup(resize_keyboard=True).row(
    errorbtn, review)).add(Admin_back)
# ----------func--------------------------


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


def get_girls_key(title):
    Girl = InlineKeyboardMarkup(row_width=2)
    girls = data.GET_GIRLS_INLINE_KEY(title)
    for i in girls:
        temp = InlineKeyboardButton(
            text=(i[0]), callback_data=i[0])
        Girl.add(temp)
    Girl.row(back)
    return Girl


# ------auto_start---------
getKey()
