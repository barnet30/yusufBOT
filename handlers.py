from main import dp,bot,db
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from config import admin_id



async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id,text="Бот запущен!☺")

#activate subscribe
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: Message):
    if (not db.subscriber_exist(message.from_user.id)):
        #если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id)
        await message.answer("Вы успешно подписаны на рассылку\nСкоро узнаете о курсе доллара☺")
    else:
        #иначе обновляем статус подписки
        db.update_subscription(message.from_user.id, True)
        await message.answer("Ваша подписка обновлена\nСкоро узнаете о курсе доллара☺")

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

#send dollar rate
@dp.message_handler(commands=['dollar'])
async def get_dollar(message: Message):
    from exrate import get_dollar
    await message.answer(f"Сейчас доллар стоит {get_dollar()} рублей")


@dp.message_handler(content_types=["text"])
async def handle_text(message):
    if "курс" in message.text.lower() or "какой курс" in message.text.lower():
        await message.answer("Вам следует подписаться на рассылку при помощи команды /subscribe"
                             " чтобы я мог уведомить вас $$")
    elif "привет" in message.text.lower() or "ку" in message.text.lower():
        await message.answer("Привет, Я ЮсуфБот!, я могу сообщать о курсе доллара)")

    elif "как дела" in message.text.lower() or "как жизнь" in message.text.lower() :
        await message.answer("У меня всё отлично, виртуально радаюсь жизни, а у тебя как? ☺")
    elif "отлично" in message.text.lower() or "хорошо" in message.text.lower():
        await message.answer("Искренне рад за вас♥")
    else:
        await message.answer("Извини я не знаю что ответить")



