from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import NewsEasyBotKeyboards as kb
from DB.manageDB import get_news, get_news_count

router = Router()

# Храним message_id отправленных новостей для каждого пользователя
user_news_messages = {}

# Храним состояния и фильтры для каждого пользователя
user_states = {}


# ----------------
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f"<b>Добро пожаловать, @{message.from_user.username}!</b>", parse_mode="html",
                        reply_markup=kb.start)


# ----------------
# Обработчик ReplyKeyboard (Новости)
@router.message(F.text == "📰Новости📰")
async def info(message: Message):
    await message.reply("<b>🏡Выберите действие: </b>", parse_mode="html", reply_markup=kb.main)


# Обработчик ReplyKeyboard (О нас)
@router.message(F.text == "💡О нас💡")
async def onas(message: Message):
    await message.reply("Команда разработчиков Pythonists")


# ----------------
# Функция для показа новостей с учетом фильтров и пагинации
async def show_filtered_news(message_or_callback, page=0, edit=False):
    user_id = message_or_callback.from_user.id

    if user_id not in user_states:
        user_states[user_id] = {'source': None, 'keyword': None}

    source = user_states[user_id].get('source')
    keyword = user_states[user_id].get('keyword')

    offset = page * 10
    news = get_news(limit=10, offset=offset, source=source, keyword=keyword)
    total_news = get_news_count(source=source, keyword=keyword)
    total_pages = (total_news + 9) // 10

    if not news:
        await message_or_callback.answer("Новостей нет :(")
        return

    # Удаляем предыдущие сообщения если нужно
    if user_id in user_news_messages:
        for msg_id in user_news_messages[user_id]:
            try:
                await message_or_callback.bot.delete_message(
                    message_or_callback.message.chat.id if edit else message_or_callback.chat.id, msg_id)
            except:
                pass
        del user_news_messages[user_id]

    sent_messages = []
    for item in news:
        news_text = f"<b>{item['category'].capitalize()}</b>\n"
        news_text += f"<i>{item['date']}</i> | {item['ist']}\n"
        news_text += f"<b>{item['short_text']}</b>\n"
        content_preview = f"{item['content'][:200]}...\n" if len(item['content']) > 200 else f"{item['content']}\n"
        news_text += content_preview
        news_text += f"<a href='{item['link']}'>Читать полностью</a>"

        if len(news_text) > 4000:
            news_text = news_text[:4000] + "... (сообщение укорочено)"
        print(f"Длина сообщения: {len(news_text)}")
        if edit:
            msg = await message_or_callback.bot.send_message(message_or_callback.message.chat.id, news_text,
                                                             parse_mode="HTML")
        else:
            msg = await message_or_callback.answer(news_text, parse_mode="HTML")
        sent_messages.append(msg.message_id)

    user_news_messages[user_id] = sent_messages

    # Кнопки пагинации с учетом фильтров
    callback_prefix = f"pag_{'s' if source else ''}{'k' if keyword else ''}_"
    pagination_msg = await message_or_callback.bot.send_message(
        message_or_callback.message.chat.id if edit else message_or_callback.chat.id,
        f"Страница {page + 1} из {total_pages}",
        reply_markup=kb.get_pagination_keyboard(page, total_pages, prefix=callback_prefix)
    )
    user_news_messages[user_id].append(pagination_msg.message_id)

# Обработчик для просмотра всех новостей
@router.callback_query(F.data == "smotr")
async def show_news(callback: CallbackQuery):
    await callback.message.edit_text("<b>👀 Смотреть новости</b>", parse_mode="html")
    await callback.message.answer("Выполняю поиск и отправляю Вам все свежие новости...")

    # получаем новости
    news = get_news()
    total_news = get_news_count()
    total_pages = (total_news + 9) // 10  # Округляем вверх

    if not news:
        await callback.message.answer("Новостей нет :(")
        return

    # отправляем новости
    sent_messages = []
    for item in news:
        news_text = f"<b>{item['category'].capitalize()}</b>\n"
        news_text += f"<i>{item['date']}</i> | {item['ist']}\n"
        news_text += f"<b>{item['short_text']}</b>\n"
        news_text += f"{item['content'][:200]}...\n" if len(item['content']) > 200 else f"{item['content']}\n"
        news_text += f"<a href='{item['link']}'>Читать полностью</a>"

        msg = await callback.message.answer(news_text, parse_mode="HTML")
        sent_messages.append(msg.message_id)

    # сохраняем ID сообщений для возможного удаления
    user_id = callback.from_user.id
    user_news_messages[user_id] = sent_messages

    # отправляем кнопки пагинации
    pagination_msg = await callback.message.answer(
        f"Страница 1 из {total_pages}",
        reply_markup=kb.get_pagination_keyboard(0, total_pages)
    )

    # сохраняем ID сообщения с пагинацией
    user_news_messages[user_id].append(pagination_msg.message_id)



# Обработчик сортировки
@router.callback_query(F.data == "sort")
async def callback_data(callback: CallbackQuery):
    await callback.message.edit_text("<b>🔎Сортировка</b>", parse_mode="html", reply_markup=kb.sort)


# Сортировка по ключевым словам
@router.callback_query(F.data == "kluch")
async def sort_by_keyword(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_states[user_id] = {'state': 'waiting_keyword', 'source': None, 'keyword': None}
    await callback.message.edit_text("Введите ключевое слово для поиска:", reply_markup=kb.back1)


@router.message(lambda message: message.from_user.id in user_states and user_states[message.from_user.id].get(
    'state') == 'waiting_keyword')
async def receive_keyword(message: Message):
    user_id = message.from_user.id
    keyword = message.text.strip()
    user_states[user_id]['keyword'] = keyword
    user_states[user_id]['state'] = None
    await message.answer(f"Ищу новости по ключевому слову '{keyword}'...")
    await show_filtered_news(message)


# Сортировка по источникам
@router.callback_query(F.data == "ist")
async def sort_by_source(callback: CallbackQuery):
    await callback.message.edit_text("Выберите источник:", reply_markup=kb.sources_keyboard)


@router.callback_query(F.data.startswith("source_"))
async def select_source(callback: CallbackQuery):
    source = callback.data.split("_")[1]
    user_id = callback.from_user.id
    user_states[user_id] = {'source': source, 'keyword': None}
    await callback.message.edit_text(f"Выбран источник: {source}")
    await show_filtered_news(callback, edit=True)


# Сортировка по источникам и ключевым словам
@router.callback_query(F.data == "oba")
async def sort_by_source_and_keyword(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_states[user_id] = {'state': 'select_source_for_oba'}
    await callback.message.edit_text("Выберите источник:", reply_markup=kb.sources_keyboard)


@router.callback_query(lambda query: query.from_user.id in user_states and user_states[query.from_user.id].get(
    'state') == 'select_source_for_oba' and query.data.startswith("source_"))
async def select_source_for_oba(callback: CallbackQuery):
    source = callback.data.split("_")[1]
    user_id = callback.from_user.id
    user_states[user_id]['source'] = source
    user_states[user_id]['state'] = 'waiting_keyword_for_oba'
    await callback.message.edit_text(f"Выбран источник: {source}. Теперь введите ключевое слово:")


@router.message(lambda message: message.from_user.id in user_states and user_states[message.from_user.id].get(
    'state') == 'waiting_keyword_for_oba')
async def receive_keyword_for_oba(message: Message):
    user_id = message.from_user.id
    keyword = message.text.strip()
    user_states[user_id]['keyword'] = keyword
    user_states[user_id]['state'] = None
    await message.answer(
        f"Ищу новости по источнику '{user_states[user_id]['source']}' и ключевому слову '{keyword}'...")
    await show_filtered_news(message)


# Обработчики пагинации (адаптированные)
# Updated handlers for pagination in NewsEasyBotHandlers.py

@router.callback_query(lambda c: 'next_' in c.data)
async def next_page(callback: CallbackQuery):
    parts = callback.data.split("_")
    next_index = parts.index('next')
    page = int(parts[next_index + 1])
    await show_filtered_news(callback, page=page + 1, edit=True)
    await callback.answer()

@router.callback_query(lambda c: 'prev_' in c.data)
async def prev_page(callback: CallbackQuery):
    parts = callback.data.split("_")
    prev_index = parts.index('prev')
    page = int(parts[prev_index + 1])
    if page > 0:
        await show_filtered_news(callback, page=page - 1, edit=True)
    await callback.answer()


# Остальные обработчики...
@router.callback_query(F.data == "news")
async def callback_data(callback: CallbackQuery):
    await callback.message.edit_text("В разработке(все новости)", parse_mode="html", reply_markup=kb.back2)


@router.callback_query(F.data == "back")
async def callback_data(callback: CallbackQuery):
    await callback.message.edit_text("<b>🏡Выберите действие: </b>", parse_mode="html", reply_markup=kb.main)


@router.callback_query(F.data == "back1")
async def callback_data(callback: CallbackQuery):
    await callback.message.edit_text("<b>🔎Сортировка</b>", parse_mode="html", reply_markup=kb.sort)


@router.callback_query(F.data == "back2")
async def callback_data(callback: CallbackQuery):
    await callback.message.edit_text("<b>🔎Сортировка</b>", parse_mode="html", reply_markup=kb.main)