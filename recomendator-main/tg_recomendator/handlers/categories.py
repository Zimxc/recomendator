from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.constants import *
from utils import db, get_genres, discover_by_genre
from keyboards import (media_list_keyboard, categories_inline_keyboard,genres_inline_keyboard,)
categories_router = Router()
@categories_router.message(Command(CATEGORIES_COMMAND))
async def cmd_categories(message: types.Message):
    categories = db.get_categories()
    
    if not categories:
        await message.answer('Немає доступних категорій')
        return
    await message.answer('Виберіть категорію:', reply_markup=categories_inline_keyboard(categories))
@categories_router.message(F.text == 'Категорії')
async def text_categories(message: types.Message):
    await cmd_categories(message)

@categories_router.callback_query(lambda c: c.data.startswith('category_'))
async def category_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    category_id = int(callback.data.split('_')[1])
    genres = get_genres(category_id)
    if not genres:
        if category_id == 1:
            media_type = 'movie'
        if category_id == 2:
            media_type = 'tv'
        else:
            media_type = 'movie'
        api_genres = await get_genres(media_type)
        if 'genres' in api_genres:
            for genre in api_genres['genres']:
                db.add_genre(genre['id'], genre['name'], category_id)
            genres = db.get_genres(category_id)
        if not genres:
            await callback.message.edit_text('Немає доступних жанрів',
            reply_markup = categories_inline_keyboard(db.get_categories()))
            return
@categories_router.callback_query(lambda c: c.data.startswith('genre_'))
async def genre_callback(callback: types.CallbackQuery):
    await callback.answer()
    _, genre_id, category_id = callback.data.split('_')
    genres = get_genres(category_id)
    genre_id = int(genre_id)

    if not genres:
        if category_id == 1:
            media_type = 'movie'
        if category_id == 2:
            media_type = 'tv'
        else:
            media_type = 'movie'