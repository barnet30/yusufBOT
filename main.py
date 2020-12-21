import asyncio
import config
import logging
from aiogram import Bot, Dispatcher, executor
from dataBase import study
from aiogram.contrib.fsm_storage.memory import MemoryStorage


loop = asyncio.get_event_loop()
#задаем уровень логов
logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
#initialization of bot
bot = Bot(token=config.API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot,loop= loop,storage=storage)

async def shutdown(dispatcher:Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

db = study('education')

#execute polling
if __name__=='__main__':
    from handlers import dp,send_to_admin
    #dp.loop.create_task(scheduled(300))
    executor.start_polling(dp,skip_updates=True,on_shutdown=shutdown)#,on_startup=send_to_admin)
