from main import dp,bot,db
from aiogram.types import Message
from config import admin_id

async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id,text="Бот запущен!☺")

#activate subscribe
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: Message):
    if (not db.subscriber_exist(message.from_user.id)):
        #если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        #иначе обновляем статус подписки
        db.update_subscription(message.from_user.id, True)
    await message.answer("Вы успешно подписаны на рассылку\nЖдите новое обновленное расписаение☺")

#deactivate subscribe
@dp.message_handler(commands=['unsubscribe'])
async def subscribe(message: Message):
    if (not db.subscriber_exist(message.from_user.id)):
        #если юзера нет в базе, добавляем его с неактивной подпиской
        db.add_subscriber(message.from_user.id,False)
        await message.answer("Вы и так не подписаны")
    else:
        #если юзер есть в базе, то меняем статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписались☺")


@dp.message_handler(content_types=["text"])
async def handle_text(message):
    if message.text == "Hi":
        await message.answer("Hello! I am YusufBot. YOU SO. How can i help you?")

    elif message.text == "How are you?" or message.text == "How are u?":
        await message.answer("I'm fine, thanks. And you?♥")

    else:
        await message.answer("Sorry, i dont understand you.")
