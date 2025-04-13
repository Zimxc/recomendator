from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils import db
from keyboards.keyboards import main_menu_keybord
from utils.constants import *

common_router = Router()
@common_router.message(Command(commands = [START_COMMAND]))
async def cmd_start(message: types.Message, state:FSMContext):
    await state.clear()
    user = message.from_user
    db.add_user(user.id,user.username,user.first_name,user.last_name)
    
    welcome_text= (
        f'👋Привіт, {user.first_name}!\n\n'
        f'🎬Вітаю у нашому боті Рекомендаторі для прегляду фільмів та серіалів'
        f'🎈Ось що я можу тобі запропонувати: \n\n'
        f'🔍Пошук фільмів та серіалів за категоріями та жанрами'
        f'🔍Перегляд трендових вільмів та серіалів\n'
        f'🔍Додавання власних фільмів та серіалів для перегляду\n\n'
        f'⏬Використовуйте кнопки меню для навігації'
        
    )
    await message.answer(welcome_text, reply_markup = main_menu_keybord)

@common_router.message(Command(commands = [HELP_COMMAND]))
@common_router.messege(F.text == ' Допомога')
async def cmd_help (message: types.Message):
    help_text = (
        'Ну не тупий же, подумай сам трошки, погугли'
    )
@common_router.message(F.text == 'Назад до меню')
async def back_to_main(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Повертаємось до головного меню',
                         reply_markup = main_menu_keybord())
def register_common_handllers(dp):
    dp.include_router(common_router)
    
