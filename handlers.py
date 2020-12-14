from main import dp,bot,db
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove
from config import admin_id
from states import RegistrationStudent, StudInCourse
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
    await RegistrationStudent.s1.set()

#
@dp.message_handler(state=RegistrationStudent.s1)
async def reg_1(message: Message,state:FSMContext):
    answer = message.text
    await state.update_data(name=answer)
    await message.answer("Введите вашу фамилию:")
    await RegistrationStudent.next()

@dp.message_handler(state=RegistrationStudent.s2)
async def reg_2(message: Message,state:FSMContext):
    answer = message.text
    await state.update_data(surname=answer)
    await message.answer("Введите номер вашей группы:")
    await RegistrationStudent.next()

@dp.message_handler(state=RegistrationStudent.s3)
async def reg_3(message: Message,state:FSMContext):
    answer = message.text
    await state.update_data(group=answer)
    await message.answer("Введите ваш возраст:")
    await RegistrationStudent.next()

@dp.message_handler(state=RegistrationStudent.s4)
async def reg_4(message: Message,state:FSMContext):
    answer = message.text
    await state.update_data(age=answer)
    await message.answer("Введите номер вашей зачётной книжки:")
    await RegistrationStudent.next()

@dp.message_handler(state=RegistrationStudent.s5)
async def reg_5(message: Message,state:FSMContext):
    answer = message.text
    await state.update_data(gradebook=answer)
    full_data = await state.get_data()
    print(full_data)

    if full_data.get("name").isalpha() and full_data.get("surname").isalpha():
        name = full_data.get("name")
        surname = full_data.get("surname")
        num_group = full_data.get("group")
        gradebook = full_data.get("gradebook")
        age = full_data.get("age")
        user_id = message.from_user.id

        await message.answer(f"Регистрация прошла успешно\n"
                             f"Ваши данные:{name},{surname},{num_group},{age},{gradebook}")
    else:
        await message.answer("Вы ввели неверные данные")
    await state.finish()

@dp.message_handler(commands=['scourse'],state=None)
async def s_join_course_begin(message:Message):
    await message.reply("Выберити курс, на который хотите записаться",
                        reply_markup=course_markup)
    await StudInCourse.states.s1.set

@dp.message_handler(state=StudInCourse.s1)
async def s_join_course_1(message:Message,state:FSMContext):
    ans = message.text
    try:
        id_course = getidcoursebyname(ans)
        check = check_stud_in_course(message.from_user.id,id_course)
        if check:
            await message.answer("Вы уже записаны на данный курс",reply_markup=ReplyKeyboardRemove())
        else:
            try:
                stud_join_course(message.from_user.id,id_course)
                await message.answer(f"Вы успешно записались на курс {ans}",reply_markup=ReplyKeyboardRemove())
    except:
        await message.answer("Упс! Что-то пошло не так, попробуй ещё раз",reply_markup=ReplyKeyboardRemove())
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




