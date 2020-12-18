from main import dp,bot,db
from aiogram.types import Message,ReplyKeyboardRemove
from keybords_button import btn_markup, btn_accept
from config import admin_id
from states import RegistrationStudent, StudInCourse, StudLeaveCourse, \
    GetAverageValues, GetWorstStudents, GetCorrelation
from aiogram.dispatcher import FSMContext
import pandas as pd
#from db_scripts import *

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
    await message.answer("Вы точно хотите зарегистрироваться на курс? ",reply_markup=btn_accept)
    await RegistrationStudent.next()

@dp.message_handler(state=RegistrationStudent.check)
async def reg_5(message: Message,state:FSMContext):
    full_data = await state.get_data()
    print(full_data)
    answer = message.text
    if (answer=="Подтвердить"):
        if full_data.get("name").isalpha() and full_data.get("surname").isalpha():
            name = full_data.get("name")
            surname = full_data.get("surname")
            num_group = full_data.get("group")
            gradebook = full_data.get("gradebook")
            age = full_data.get("age")
            user_id = message.from_user.id
            try:
                db.add_new_student(user_id,name,surname,age,num_group,gradebook)
                await message.answer("Регистрация прошла успешно!☺",reply_markup=ReplyKeyboardRemove())
            except:
                await message.answer("Вы уже зарегистрированны в системе",reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer("Вы ввели неверные данные",reply_markup=ReplyKeyboardRemove())
    await state.finish()

@dp.message_handler(commands=['scourse'],state=None)
async def s_join_course_begin(message:Message):
    await message.reply("Выберити курс, на который хотите записаться",
                        reply_markup=btn_markup)
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
    await message.answer("Какой курс вы хотите покинуть?",reply_markup=btn_markup)
    await StudLeaveCourse.s1.set()


@dp.message_handler(state=StudLeaveCourse.s1)
async def sleave1(message:Message, state:FSMContext):
    course_name = message.text
    id_course = db.get_id_course_by_name(course_name)
    check = db.check_stud_in_course(message.from_user.id,id_course)
    if not check:
        await message.answer("Вас нет в списке студентов данного курса",reply_markup=ReplyKeyboardRemove())
        await state.finish()
    try:
        db.del_stud_from_course(message.from_user.id,id_course)
        await message.answer(f"Вы были удалены из курса {course_name}.\n",reply_markup=ReplyKeyboardRemove())
    except:
        await message.answer("Вас нет в списке студентов данного курса",reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(commands=['getaveragevalues'],state=None)
async def enter_course_stats(message:Message):
    await message.reply("Выберите предмет, по которому Вы хотите получить средние показатели", reply_markup=btn_markup)
    await GetAverageValues.s1.set()


@dp.message_handler(state=GetAverageValues.s1)
async def answer_q1(message: Message, state: FSMContext):
    try:
        answer = message.text
        cid = db.get_id_course_by_name(answer)
        list_of_students = db.get_list_of_students(cid)
        n=len(list_of_students)
        grades_sum=0
        ages_sum=0
        couples_list=[]
        couples_sum=0
        for student in list_of_students:
            grades_sum+=sum(db.get_grades(student[0],cid))
            ages_sum+=db.get_age(student[0])
            couples_list=db.get_attendence(student[0],cid)
            for couple in couples_list:
                if couple=="Н" or couple=="У":
                    pass
                else:
                    couples_sum+=1
        if n==0:
            await message.answer("Нет студентов на данном курсе")
        elif len(couples_list)==0:
            await message.answer("Занятий ещё не проводилось"+
                                "Средний возраст студентов: "+
                                str(ages_sum/n))
        else:
            await message.answer("Средний балл за курс: "+
                                str(grades_sum/n)+
                                "Средняя посещаемость: "+
                                str(couples_sum/(n*len(couples_list)))+"%"+
                                "Средний возраст студентов: "+
                                str(ages_sum/n))
    except:
        await message.answer("Произошла непредвиденная ошибка")
    await state.finish()

@dp.message_handler(commands=['getworststudents'],state=None)
async def get_top5(message: Message):
    await message.reply("Выберите предмет, по которому Вы хотите полученить данные о студентах, у которых не хватает баллов до зачёта", reply_markup=btn_markup)
    await GetWorstStudents.s1.set()


@dp.message_handler(state=GetWorstStudents.s1)
async def answer_q1(message: Message, state: FSMContext):
    try:
        answer = message.text
        cid = db.get_id_course_by_name(answer)
        list_of_students = db.get_list_of_students(cid)
        worst_students=""
        for student in list_of_students:
            if sum(db.get_grades(student[0],cid))<56:
                worst_students=worst_students+f"{student[1]} {student[2]} : {sum(db.get_grades(student[0],cid))}\n"
        if len(list_of_students)==0:
            await message.answer("Нет студентов на данном курсе")
        else:
            await message.answer(worst_students)
    except:
        await message.answer("Произошла непредвиденная ошибка")
    await state.finish()


@dp.message_handler(commands=['getcorrelation'],state=None)
async def enter_course_stats(message: Message):
    await message.reply("Выберите предмет, по которому Вы хотите получить корреляционную зависимость", reply_markup=btn_markup)
    await GetCorrelation.s1.set()


@dp.message_handler(state=GetCorrelation.s1)
async def answer_q1(message: Message, state: FSMContext):
    try:
        answer = message.text
        cid = db.get_id_course_by_name(answer)
        list_of_students = db.get_list_of_students(cid)
        n=len(list_of_students)
        grades_list=[]
        attendence_list=[]
        ages_list=[]
        couples_list=[]
        for student in list_of_students:
            grades_list.append(db.get_grades(student[0],cid))
            couples_list=db.get_attendence(student[0],cid)
            couples_sum=0
            ages_list.append(db.get_age(student[0]))
            for couple in couples_list:
                if couple=="Н" or couple=="У":
                    pass
                else:
                    couples_sum+=1
            attendence_list.append(couples_sum)

        grades_list=pd.Series(grades_list)
        attendence_list=pd.Series(attendence_list)
        ages_list=pd.Series(ages_list)
        if n==0:
            await message.answer("Нет студентов на данном курсе")
        elif len(couples_list)==0:
            await message.answer("Занятий ещё не проводилось")
        else:
            await message.answer("Коэффециент корреляции между оценками и посещаемость: "+
                                str(grades_list.corr(attendence_list))+
                                "Коэффециент корреляции между оценками и возрастом: "+
                                str(grades_list.corr(ages_list))+
                                "Коэффециент корреляции между посещаемостью и возрастом: "+
                                str(attendence_list.corr(ages_list)))
    except:
        await message.answer("Произошла непредвиденная ошибка")
    await state.finish()

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




