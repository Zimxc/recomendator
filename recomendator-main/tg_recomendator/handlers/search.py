from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from states import SearchState
from utils.constants import *
from states import SearchStates
from utils import search_movie, search_tv
from keyboards import media_list_keyboard, main_menu_keybord
from keyboards import cancel_keyboard

search_router = Router()


@search_router.message(Command(commands=[SEARCH_COMMAND]))
async def cmd_search(message: types.Message, state: FSMContext):
    await state.set_state(SearchState.waiting_for_query)
    await message.answer('Введіть назву фільму або серіалу для пошуку', reply_markup=cancel_keyboard('cancel_search'))
@search_router.message(F.text == 'Пошук')
async def search_movie(message: types.Message, state: FSMContext):
    await cmd_search(message, state)

@search_router.message(StateFilter(SearchState.waiting_for_query))
async def process_query(message: types.Message, state: FSMContext):
    query = message.text
    if not query:
        await message.answer('Введіть назву фільму або серіалу для пошуку', reply_markup=cancel_keyboard('cancel_search'))
        return
    search_message = await message.answer('Пошук...')
    movies_result = await search_movie(query)
    tv_result = await search_tv(query)

    await state.clear()
    
    movie_count = len(movies_result.get('results', [])) if movies_result else 0
    tv_count = len(tv_result.get('results', [])) if tv_result else 0
    
    if movie_count == 0 and tv_count == 0:
        await search_message.edit_text('Фільм або серіал не знайдено')
    text = f'Результати пошуку за запитом "{query}":\n\n'
    if movie_count > 0:
        text += f'Фільми: {movie_count}\n'
        for movie in enumerate(movies_result['results'][:5],1):
            title = movie.get('title', movie.get('title', 'Невідома назва'))
            release_date = movie.get('release_date','')
            release_year = f'({release_date[:4]})' if release_date else ''
            rating = movie.get('vote_average', 0)
            rating_stars = '⭐' * int(rating/2) if rating else ''
            text += f'{title} {release_year} - {rating_stars} {rating}\n'
    
    if tv_count > 5 :
        text = f'... і ще {tv_count} фільмів'
    text += '\n'
    if tv_count > 0:
        text += f'Серіалів знайдено: {tv_count}\n'
        for i, tv in enumerate(tv_result['results'][:5], 1):
            title = tv.get('name', 'Невідома назва')
            first_air_date = tv.get('first_air_date','')
            release_date = f'({first_air_date[:4]})' if first_air_date else ''
            rating = tv.get('vote_average', 0)
            rating_stars = '⭐' * int(rating/2) if rating else ''
    if tv_count > 5:
        text = f'... і ще {tv_count} серіалів'
    await search_message.edit_text(text, parse_code = "HTML")
@search_router.callback_query(lambda c: c.data == 'cancel_search')
async def cancel_search(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.clear()
    await callback_query.message.edit_text('Пошук відмінено')
def register_search_handlers(dp):
    dp.include_router(search_router)