# NewsEasyBotHandlers.py
import time
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

import NewsEasyBotKeyboards as kb
from DB.manageDB import get_news, get_news_count

router = Router()

# Храним message_id отправленных новостей для каждого пользователя
user_news_messages = {}


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
# Обработчик callback_data Inline-кнопок (main)
@router.callback_query(F.data == "smotr")
async def show_news(callback: CallbackQuery):
    await callback.message.edit_text("<b>👀 Смотреть новости</b>", parse_mode="html")
    await callback.message.answer("Выполняю поиск и отправляю Вам все свежие новости...")

    # Получаем новости
    news = get_news()
    total_news = get_news_count()
    total_pages = (total_news + 9) // 10  # Округляем вверх

    if not news:
        await callback.message.answer("Новостей нет :(")
        return

    # Отправляем новости
    sent_messages = []
    for item in news:
        news_text = f"<b>{item['category'].capitalize()}</b>\n"
        news_text += f"<i>{item['date']}</i> | {item['ist']}\n"
        news_text += f"<b>{item['short_text']}</b>\n"
        news_text += f"{item['content'][:200]}...\n" if len(item['content']) > 200 else f"{item['content']}\n"
        news_text += f"<a href='{item['link']}'>Читать полностью</a>"

        msg = await callback.message.answer(news_text, parse_mode="HTML")
        sent_messages.append(msg.message_id)

    # Сохраняем ID сообщений для возможного удаления
    user_id = callback.from_user.id
    user_news_messages[user_id] = sent_messages

    # Отправляем кнопки пагинации
    pagination_msg = await callback.message.answer(
        f"Страница 1 из {total_pages}",
        reply_markup=kb.get_pagination_keyboard(0, total_pages)
    )

    # Сохраняем ID сообщения с пагинацией
    user_news_messages[user_id].append(pagination_msg.message_id)


# Обработчики для пагинации
@router.callback_query(F.data.startswith("next_"))
async def next_page(callback: CallbackQuery):
    page = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    # Удаляем предыдущие сообщения
    if user_id in user_news_messages:
        for msg_id in user_news_messages[user_id]:
            try:
                await callback.bot.delete_message(callback.message.chat.id, msg_id)
            except:
                pass  # Игнорируем ошибки удаления
        del user_news_messages[user_id]

    # Получаем новые новости
    offset = (page + 1) * 10
    news = get_news(offset=offset)
    total_news = get_news_count()
    total_pages = (total_news + 9) // 10

    if not news:
        await callback.answer("Больше новостей нет")
        return

    # Отправляем новые новости
    sent_messages = []
    for item in news:
        news_text = f"<b>{item['category'].capitalize()}</b>\n"
        news_text += f"<i>{item['date']}</i> | {item['ist']}\n"
        news_text += f"<b>{item['short_text']}</b>\n"
        news_text += f"{item['content'][:200]}...\n" if len(item['content']) > 200 else f"{item['content']}\n"
        news_text += f"<a href='{item['link']}'>Читать полностью</a>"

        msg = await callback.message.answer(news_text, parse_mode="HTML")
        sent_messages.append(msg.message_id)

    # Сохраняем ID новых сообщений
    user_news_messages[user_id] = sent_messages

    # Отправляем новые кнопки пагинации
    pagination_msg = await callback.message.answer(
        f"Страница {page + 2} из {total_pages}",
        reply_markup=kb.get_pagination_keyboard(page + 1, total_pages)
    )

    # Сохраняем ID сообщения с пагинацией
    user_news_messages[user_id].append(pagination_msg.message_id)
    await callback.answer()


@router.callback_query(F.data.startswith("prev_"))
async def prev_page(callback: CallbackQuery):
    page = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    # Удаляем текущие сообщения
    if user_id in user_news_messages:
        for msg_id in user_news_messages[user_id]:
            try:
                await callback.bot.delete_message(callback.message.chat.id, msg_id)
            except:
                pass  # Игнорируем ошибки удаления
        del user_news_messages[user_id]

    # Получаем предыдущие новости
    offset = (page - 1) * 10
    news = get_news(offset=offset)
    total_news = get_news_count()
    total_pages = (total_news + 9) // 10

    # Отправляем новые новости
    sent_messages = []
    for item in news:
        news_text = f"<b>{item['category'].capitalize()}</b>\n"
        news_text += f"<i>{item['date']}</i> | {item['ist']}\n"
        news_text += f"<b>{item['short_text']}</b>\n"
        news_text += f"{item['content'][:200]}...\n" if len(item['content']) > 200 else f"{item['content']}\n"
        news_text += f"<a href='{item['link']}'>Читать полностью</a>"

        msg = await callback.message.answer(news_text, parse_mode="HTML")
        sent_messages.append(msg.message_id)

    # Сохраняем ID новых сообщений
    user_news_messages[user_id] = sent_messages

    # Отправляем новые кнопки пагинации
    pagination_msg = await callback.message.answer(
        f"Страница {page} из {total_pages}",
        reply_markup=kb.get_pagination_keyboard(page - 1, total_pages)
    )

    # Сохраняем ID сообщения с пагинацией
    user_news_messages[user_id].append(pagination_msg.message_id)
    await callback.answer()


# Остальные обработчики...
@router.callback_query(F.data == "sort")
async def callback_data(callback: CallbackQuery):
    await callback.message.edit_text("<b>🔎Сортировка</b>", parse_mode="html", reply_markup=kb.sort)


@router.callback_query(F.data == "news")
async def callback_data(callback: CallbackQuery):
    await callback.message.edit_text("В разработке(все новости)", parse_mode="html", reply_markup=kb.back2)


@router.callback_query(F.data == "kluch")
async def callback_data(callback: CallbackQuery):
    await callback.message.edit_text("В разработке(сортировка по ключевым словам)", parse_mode="html",
                                     reply_markup=kb.back1)


@router.callback_query(F.data == "ist")
async def callback_data(callback: CallbackQuery):
    await callback.message.edit_text("В разработке(сортировка по источникам)", parse_mode="html", reply_markup=kb.back1)


@router.callback_query(F.data == "oba")
async def callback_data(callback: CallbackQuery):
    await callback.message.edit_text("В разработке(сортировка по ключевым словам и источникам)", parse_mode="html",
                                     reply_markup=kb.back1)


@router.callback_query(F.data == "back")
async def callback_data(callback: CallbackQuery):
    await callback.message.edit_text("<b>🏡Выберите действие: </b>", parse_mode="html", reply_markup=kb.main)


@router.callback_query(F.data == "back1")
async def callback_data(callback: CallbackQuery):
    await callback.message.edit_text("<b>🔎Сортировка</b>", parse_mode="html", reply_markup=kb.sort)


@router.callback_query(F.data == "back2")
async def callback_data(callback: CallbackQuery):
    await callback.message.edit_text("<b>🔎Сортировка</b>", parse_mode="html", reply_markup=kb.main)