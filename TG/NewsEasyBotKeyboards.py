#NewsEasyBotKeyboards.py

# файл со всеми клавиатурами, тоже Кристиан шарит. единственное, что я добавил функцию для клавиатуры с пагинацией по страницам

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
#================



#================
# Add to NewsEasyBotKeyboards.py
sources_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="РБК Новости", callback_data="source_РБК Новости")],
    [InlineKeyboardButton(text="РБК Инвестиции", callback_data="source_РБК Инвестиции")],
   [InlineKeyboardButton(text="Лента.ру", callback_data="source_Lenta.ru")],
    [InlineKeyboardButton(text="Interfax", callback_data="source_Interfax.ru")],
    [InlineKeyboardButton(text="Назад", callback_data="back1")]
])

def get_pagination_keyboard(current_page, total_pages, prefix=""):
    keyboard = []
    if current_page > 0:
        keyboard.append(InlineKeyboardButton(text="◀️ Предыдущая", callback_data=f"{prefix}prev_{current_page}"))
    if current_page < total_pages - 1:
        keyboard.append(InlineKeyboardButton(text="Следующая ▶️", callback_data=f"{prefix}next_{current_page}"))
    return InlineKeyboardMarkup(inline_keyboard=[keyboard])

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