from main import dp,bot,db
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from config import admin_id
from states import RegistrationInSystem
from aiogram.dispatcher import FSMContext

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



#registration
@dp.message_handler(commands=['registration'],state=None)
async def reg_begin(message: Message):
    await message.answer("Введите ваше имя:")
    await RegistrationInSystem.s1.set()

#
@dp.message_handler(state=RegistrationInSystem.s1)
async def reg_answer1(message: Message,state:FSMContext):
    answer = message.text
    await state.update_data(name=answer)
    await message.answer("Введите вашу фамилию:")
    await RegistrationInSystem.next()

@dp.message_handler(state=RegistrationInSystem.s2)
async def reg_answer2(message: Message,state:FSMContext):
    answer = message.text
    await state.update_data(surname=answer)
    await message.answer("Введите номер вашей группы:")
    await RegistrationInSystem.next()

@dp.message_handler(state=RegistrationInSystem.s3)
async def reg_answer3(message: Message,state:FSMContext):
    answer = message.text
    await state.update_data(group=answer)
    await message.answer("Введите номер вашего студенческого билета:")
    await RegistrationInSystem.next()

@dp.message_handler(state=RegistrationInSystem.s4)
async def reg_answer4(message: Message,state:FSMContext):
    answer = message.text
    await state.update_data(stud_card=answer)
    full_data = await state.get_data()
    print(full_data)

    if full_data.get("name").isalpha() and full_data.get("surname").isalpha():
        name = full_data.get("name")
        surname = full_data.get("surname")
        num_group = full_data.get("group")
        stud_card = full_data.get("stud_card")
        user_id = message.from_user.id

        await message.answer(f"Регистрация прошла успешно\n"
                             f"Ваши данные:{name},{surname},{num_group},{stud_card}")
    else:
        await message.answer("Вы ввели неверные данные")
    await state.finish()



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




