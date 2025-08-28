#projectBOT
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher
from RBK.RBK_invest import parse_rbk_invest
from RBK.RBK_news import parse_rbk_news
from NewsEasyBotHandlers import router

load_dotenv()

token = os.getenv("TOKEN")

#--------------------------------
async def run_parsers():
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, parse_rbk_news)
        await loop.run_in_executor(None, parse_rbk_invest)
        print("Парсеры успешно выполнились")
    except Exception as e:
        print(f"Ошибка в парсерах: {e}")


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_parsers, 'interval', minutes=15)
    scheduler.start()
    bot = Bot(token=token)

    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    try:
        await asyncio.Future()
    finally:
        scheduler.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Остановка бота.")