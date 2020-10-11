import asyncio
import config
import logging
from aiogram import Bot, Dispatcher, executor, types

from subs import subscribers

loop = asyncio.get_event_loop()
#задаем уровень логов
logging.basicConfig(level=logging.INFO)

#initialization of bot
bot = Bot(token=config.API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot,loop= loop)

#initializing db
db = subscribers('subsdb.db')

#activate subscribe
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if (not db.subscriber_exist(message.from_user.id)):
        #если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        #иначе обновляем статус подписки
        db.update_subscription(message.from_user.id, True)
    await message.answer("Вы успешно подписаны на рассылку\nЖдите новое обновленное расписаение☺")

@dp.message_handler(commands=['unsubscribe'])
async def subscribe(message: types.Message):
    if (not db.subscriber_exist(message.from_user.id)):
        #если юзера нет в базе, добавляем его с неактивной подпиской
        db.add_subscriber(message.from_user.id,False)
        await message.answer("Вы и так не подписаны")
    else:
        #если юзер есть в базе, то меняем статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписались☺")



#execute polling
if __name__=='__main__':
    from handlers import dp,send_to_admin
    executor.start_polling(dp,skip_updates=True,on_startup=send_to_admin)
