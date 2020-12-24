from loader import bot,dp
from config import admin_id
from aiogram.types import Message

@dp.message_handler(commands=["help"])
async def help(message):
    await message.answer("""🎓🎓🎓 КОМАНДЫ ДОСТУПНЫЕ ДЛЯ СТУДЕНТА: 🎓🎓🎓 \n
    1)reg_stud - регистрация студента в системе \n
    2)scourse - записаться на курс \n
    3)getaveragevalues - получить средние оценки \n
    4)getworststudents - получить список должников \n
    5)getmyoverall - получить общий балл по курсу \n
    6)getcorrelation - корреляционная зависимость \n
    7)getmygrades - получить мои оценки \n
    8)myinfo - получить информацию о себе \n
    9)leavecourse - покинуть курс \n
    **** КОМАНДЫ ДЛЯ ПРЕПОДАВАТЕЛЯ: ****\n
    1)reg_teacher - регистрация преподавателя в системе \n
    2)tcourse - запись преподавателя на курс \n
    3)getjournal - получить журнал с оценками \n
    4)fillgrades - заполнить журнал с оценками \n
    5)getattendencejournal - получить журнал с посещаемостью \n
    6)fillattendence - заполнить журнал с посещаемостью \n
    """)


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id,text="Бот запущен!☺")

@dp.message_handler(commands=["start"])
async def start(message:Message):
    await message.answer("Привет, Я ЮсуфБот! Я помогаю студентам и преподавателям "
                             "с учебным процессом ☺\n"
                         "Для списка команд используйте команду /help")

@dp.message_handler(commands=["text"])
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
