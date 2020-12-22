from loader import bot,dp
from config import admin_id



async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id,text="Бот запущен!☺")


@dp.message_handler(content_types=["text"])
async def handle_text(message):

    if "привет" in message.text.lower() or "ку" in message.text.lower():
        await message.answer("Привет, Я ЮсуфБот! Я помогаю студентам и преподавателям "
                             "с учебным процессом ☺")

    elif "как дела" in message.text.lower() or "как жизнь" in message.text.lower() :
        await message.answer("У меня всё отлично - клубнично, а у тебя как? ☺")
    elif "отлично" in message.text.lower() or "хорошо" in message.text.lower():
        await message.answer("Искренне рад за тебя♥")
    elif "лох" in message.text.lower() or "не оч"in message.text.lower():
        await  message.answer("Попей тёплый чай и займись недоделанными делами")
    else:
        await message.answer("Извини я не знаю что ответить")
