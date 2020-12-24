from loader import bot,dp
from config import admin_id
from aiogram.types import Message


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id,text="Бот запущен!☺")

@dp.message_handler(content_types=["start"])
async def start(message:Message):
    await message.answer("Привет, Я ЮсуфБот! Я помогаю студентам и преподавателям "
                             "с учебным процессом ☺\n"
                         "Для списка команд используйте команду /help")

@dp.message_handler(content_types=["text"])
async def handle_text(message:Message):

    if "привет" in message.text.lower() or "ку" in message.text.lower():
        await message.answer("Привет, Я ЮсуфБот! Я помогаю студентам и преподавателям "
                             "с учебным процессом ☺")

    elif "как дела" in message.text.lower() or "как жизнь" in message.text.lower() :
        await message.answer("У меня всё отлично - клубнично, а у тебя как? ☺")
    elif "отлично" in message.text.lower() or "хорошо" in message.text.lower():
        await message.answer("Искренне рад за тебя♥")
    elif "лох" in message.text.lower() or "не оч"in message.text.lower():
        await  message.answer("Попей тёплый чай и ляг поспи реально")
    # elif "дан" in message.text.lower():
    #     await bot.send_message(chat_id=1463929248,text="Kak dela")
    else:
        await message.answer("Извини я не знаю что ответить")
