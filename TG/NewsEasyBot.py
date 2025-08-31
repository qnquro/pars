#projectBOT
#основной файл который всё запускает
import os
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler # нужно для того чтобы и бот и парсеры работали одновременно
from dotenv import load_dotenv # для работы в .env файлами(кто не знает что это - прочитайте в инете)
from aiogram import Bot, Dispatcher
from parsers.RBK.RBK_invest import parse_rbk_invest
from parsers.RBK.RBK_news import parse_rbk_news
from parsers.INTERFAX.INTERFAX import parse_interfax_ru_sync
from parsers.LENTA.LENTA import parse_lenta_ru_sync
from NewsEasyBotHandlers import router

load_dotenv() # нашли .env файл

token = os.getenv("TOKEN") # достали из .env файла token

#--------------------------------
# функция для того, чтобы запускать парсеры
async def run_parsers():
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, parse_lenta_ru_sync())
        await loop.run_in_executor(None, parse_interfax_ru_sync())
        await loop.run_in_executor(None, parse_rbk_news)
        await loop.run_in_executor(None, parse_rbk_invest)

        print("Парсеры успешно выполнились")
    except Exception as e:
        print(f"Ошибка в парсерах: {e}")

# ну не зря это main функция, она всё запускает
async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_parsers, 'interval', minutes=15) #создал параллельный асинхронный поток для функции run_parsers, который будет запускать её раз в 15 минут
    scheduler.start() # запустил поток
    bot = Bot(token=token)

    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    try:
        await asyncio.Future() #бесконечный цикл
    finally:
        scheduler.shutdown() #выключение потока в случае остановки бота


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Остановка бота.")