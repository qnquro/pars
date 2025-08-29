#NewsEasyBotKeyboards.py

# файл со всеми клавиатурами, тоже Кристиан шарит. единственное, что я добавил функцию для клавиатуры с пагинацией по страницам

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
#================



#================
start = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📰Новости📰")],[KeyboardButton(text="💡О нас💡")]], 
									resize_keyboard=True, 
									input_field_placeholder="Выберите пункт меню")

main = InlineKeyboardMarkup(inline_keyboard=[
						[InlineKeyboardButton(text="👀Смотреть все новости", callback_data="smotr")], 
						[InlineKeyboardButton(text="🔎Сортировка", callback_data="sort")]




						])




sort = InlineKeyboardMarkup(inline_keyboard=[
					[InlineKeyboardButton(text="По ключевым словам", callback_data="kluch")],
					[InlineKeyboardButton(text="По источникам", callback_data="ist")],
					[InlineKeyboardButton(text="По ключевым словам и источникам", callback_data="oba")],
					[InlineKeyboardButton(text="⬅️", callback_data="back")]



	])

back1 =  InlineKeyboardMarkup(inline_keyboard=[
					[InlineKeyboardButton(text="⬅️", callback_data="back1")]



	])

back2 =  InlineKeyboardMarkup(inline_keyboard=[
					[InlineKeyboardButton(text="⬅️", callback_data="back2")]



	])


def get_pagination_keyboard(page=0, total_pages=1):
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"prev_{page}"))

    if page < total_pages - 1:
        buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"next_{page}"))

    return InlineKeyboardMarkup(inline_keyboard=[buttons])