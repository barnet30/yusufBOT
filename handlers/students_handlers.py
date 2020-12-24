from main import db
from loader import dp
from aiogram.types import Message,ReplyKeyboardRemove
from states import RegistrationStudent, StudInCourse, StudLeaveCourse, GetOverall, GetGrades
from aiogram.dispatcher import FSMContext
from keybords_button import course_keyboard, accept_keyboard
import traceback




@dp.message_handler(commands=['reg_stud'],state=None)
async def reg_begin(message: Message):
    await message.answer("Введите ваше имя:")
    await RegistrationStudent.name.set()


@dp.message_handler(state=RegistrationStudent.name)
async def reg_1(message: Message,state:FSMContext):
    answer = message.text
    await state.update_data(name=answer)
    await message.answer("Введите вашу фамилию:")
    await RegistrationStudent.next()

@dp.message_handler(state=RegistrationStudent.surname)
async def reg_2(message: Message,state:FSMContext):
    answer = message.text
    await state.update_data(surname=answer)
    await message.answer("Введите номер вашей группы:")
    await RegistrationStudent.next()

@dp.message_handler(state=RegistrationStudent.group)
async def reg_3(message: Message,state:FSMContext):
    answer = message.text
    await state.update_data(group=answer)
    await message.answer("Введите ваш возраст:")
    await RegistrationStudent.next()

@dp.message_handler(state=RegistrationStudent.age)
async def reg_4(message: Message,state:FSMContext):
    answer = message.text
    await state.update_data(age=answer)
    await message.answer("Введите номер вашей зачётной книжки:")
    await RegistrationStudent.next()



@dp.message_handler(state=RegistrationStudent.gradebook)
async def reg_5(message: Message,state:FSMContext):
    answer = message.text
    await state.update_data(gradebook=answer)
    full_data = await state.get_data()
    await message.answer("Вы точно хотите зарегистрироваться на курс?\n"
                         "Введённые вами данные:\n"
                         f"Имя: {full_data.get('name')}, Фамилия: {full_data.get('surname')}, "
                         f"Номер группы: {full_data.get('group')}, Возраст: {full_data.get('age')}, "
                         f"Номер зачётной книжки: {full_data.get('gradebook')} ",reply_markup=accept_keyboard)
    await RegistrationStudent.next()

@dp.message_handler(state=RegistrationStudent.check)
async def reg_6(message: Message,state:FSMContext):
    answer = message.text
    if (answer=="Подтвердить"):
        full_data = await state.get_data()
        print(full_data)
        if full_data.get("name").isalpha() and full_data.get("surname").isalpha():
            name = full_data.get("name")
            surname = full_data.get("surname")
            num_group = full_data.get("group")
            gradebook = full_data.get("gradebook")
            age = full_data.get("age")
            user_id = message.from_user.id
            try:
                db.add_new_student(user_id,name,surname,gradebook,num_group,age)
                await message.answer("Регистрация прошла успешно!☺",reply_markup=ReplyKeyboardRemove())
            except:
                await message.answer("Вы уже зарегистрированны в системе",reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer("Вы ввели неверные данные",reply_markup=ReplyKeyboardRemove())
    elif(answer=="Изменить данные"):
        await message.answer("Введите ваше имя:",reply_markup=ReplyKeyboardRemove())
        await RegistrationStudent.name.set()
        return
    await state.finish()


@dp.message_handler(commands=['scourse'],state=None)
async def s_join_course_begin(message:Message):
    await message.reply("Выберити курс, на который хотите записаться",
                        reply_markup=course_keyboard)
    await StudInCourse.s1.set()

@dp.message_handler(state=StudInCourse.s1)
async def s_join_course_1(message:Message,state:FSMContext):
    course_name = message.text
    try:
        id_course = db.get_id_course_by_name(course_name)
        check = db.check_stud_in_course(message.from_user.id,id_course)
        if check:
            await message.answer("Вы уже записаны на данный курс",reply_markup=ReplyKeyboardRemove())
        else:
            try:
                db.stud_join_course(message.from_user.id,id_course)
                await message.answer(f"Вы успешно записались на курс {course_name}",reply_markup=ReplyKeyboardRemove())
            except:
                await message.answer("Что-то пошло не так..",reply_markup=ReplyKeyboardRemove())
    except:
        await message.answer("Упс! Что-то пошло не так, попробуй ещё раз",reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(commands=['leavecourse'],state=None)
async def sleave_begin(message:Message):
    await message.answer("Какой курс вы хотите покинуть?",reply_markup=course_keyboard)
    await StudLeaveCourse.s1.set()


@dp.message_handler(state=StudLeaveCourse.s1)
async def sleave1(message:Message, state:FSMContext):
    course_name = message.text
    id_course = db.get_id_course_by_name(course_name)
    check = db.check_stud_in_course(message.from_user.id,id_course)
    if not check:
        await message.answer("Вас нет в списке студентов данного курса",reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return
    try:
        db.del_stud_from_course(message.from_user.id,id_course)
        await message.answer(f"Вы были удалены из курса {course_name}.\n",reply_markup=ReplyKeyboardRemove())
    except:
        await message.answer("Вас нет в списке студентов данного курса",reply_markup=ReplyKeyboardRemove())
    await state.finish()

@dp.message_handler(commands=['getmyoverall'],state=None)
async def enter_course_stats(message:Message):
    await message.reply("По какому предмету вы хотите получить общий балл?", reply_markup=course_keyboard)
    await GetOverall.s1.set()

@dp.message_handler(state=GetOverall.s1)
async def answer_q1(message: Message, state: FSMContext):
    course_name = message.text
    try:
        cid = db.get_id_course_by_name(course_name)
        score = db.get_grades(message.from_user.id,cid)
        itog_score=0
        for i in score:
            itog_score+=i
        await message.answer("Ваш балл по курсу: " + str(itog_score), reply_markup=ReplyKeyboardRemove())
    except:
        await message.answer("Произошла непредвиденная ошибка")
    await state.finish()

##############
@dp.message_handler(commands=['getmygrades'],state=None)
async def enter_course_stats(message:Message):
    await message.reply("По какому предмету вы хотите получить оценки?", reply_markup=course_keyboard)
    await GetGrades.s1.set()

@dp.message_handler(state=GetGrades.s1)
async def answer_q1(message: Message, state: FSMContext):
    course_name = message.text
    try:
        cid = db.get_id_course_by_name(course_name)
        score = db.get_grades(message.from_user.id,cid)
        scores=[]
        for i in score:
            scores.append(i)
        await message.answer("Ваши оценки по курсу: " + ' '.join(str(scores)), reply_markup=ReplyKeyboardRemove())
    except:
        await message.answer("Произошла непредвиденная ошибка")
    await state.finish()
#################

@dp.message_handler(commands=['myinfo'])
async def get_stud_info(message:Message):
    try:
        student = db.get_stud_info(message.from_user.id)
        await message.answer("Ваши данные:\n"
                       f"Фамилия: {student[2]}\nИмя: {student[1]}\nНомер зачётной книжки: {student[3]}\nГруппа: {student[4]}\nВозраст: {student[5]}")
    except:
        await message.answer("Вы ещё не зарегистрированы!\nИспользуйте команду /reg_stud , чтобы зарегистрироваться!")