#projectBOT
import os

from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher

from NewsEasyBotHandlers import router 

load_dotenv()

token = os.getenv("TOKEN")

#--------------------------------
async def main():
	bot = Bot(token=token)

	dp = Dispatcher()
	dp.include_router(router)
	await dp.start_polling(bot)




if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print("Остановка бота.")
        while True:
