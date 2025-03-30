from aiogram import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)
from utils.constants import *

def main_meny_keybord():
    buttons = [
        [KeyboardButton(text='🎭Категорії'), KeyboardButton(text = '🔍Пошук')],
        [KeyboardButton(text='🔥Популряне'), KeyboardButton(text = '❓Допомога')],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
    )
    return keyboard
def admin_keyboard():
    buttons = [
        [KeyboardButton(text='🛠Додати жанр')]
        [KeyboardButton(text='🛠Додати катергорію')],
        [KeyboardButton(text='🛠Додати фільм/серіал')],
        [KeyboardButton(text='✔Назад до меню')],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
    )
def categories_inline_keyboard(categories):
    buttons = []
    for category in categories:
        buttons.append([InlineKeyboardButton(text=category['name'], callback_data=f'category_{category["id"]}')])
    buttons.append([InlineKeyboardButton(text='🔙Назад', callback_data='back_to_main')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard