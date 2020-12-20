from main import dp,bot,db
from aiogram.types import Message,ReplyKeyboardRemove
from keybords_button import course_keyboard, accept_keyboard, choice_keyboard
from config import admin_id
from states import RegistrationStudent, StudInCourse, StudLeaveCourse, GetOverall, \
    GetAverageValues, GetWorstStudents, GetCorrelation, RegistrationTeacher,\
    TeacherInCourse, GetJournal,GetAttendenceJournal,FillGrades,FillAttendence
from aiogram.dispatcher import FSMContext
import pandas as pd
import math
import traceback

async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id,text="Бот запущен!☺")

#registration
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
    await message.answer("Вы точно хотите зарегистрироваться на курс? ",reply_markup=accept_keyboard)
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
        await message.answer("Введите ваше имя:")
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




@dp.message_handler(commands=['getaveragevalues'],state=None)
async def enter_course_stats(message:Message):
    await message.reply("Выберите предмет, по которому Вы хотите получить средние показатели", reply_markup=course_keyboard)
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
                                "\nСредняя посещаемость: "+
                                str(couples_sum/(n*len(couples_list))*100)+"%"+
                                "\nСредний возраст студентов: "+
                                str(ages_sum/n))
    except:
        await message.answer("Произошла непредвиденная ошибка")
    await state.finish()

@dp.message_handler(commands=['getworststudents'],state=None)
async def get_top5(message: Message):
    await message.reply("Выберите предмет, по которому Вы хотите полученить данные о студентах, у которых не хватает баллов до зачёта", reply_markup=course_keyboard)
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
async def course_corr_begin(message: Message):
    await message.reply("Выберите предмет, по которому Вы хотите получить корреляционную зависимость", reply_markup=course_keyboard)
    await GetCorrelation.s1.set()


@dp.message_handler(state=GetCorrelation.s1)
async def course_corr1(message: Message, state: FSMContext):
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
            grades_list.append(sum(db.get_grades(student[0],cid)))
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


@dp.message_handler(commands=['reg_teacher'],state=None)
async def reg_teacher_begin(message:Message):
    await message.answer("Введите ваше имя:")
    await RegistrationTeacher.name.set()

@dp.message_handler(state=RegistrationTeacher.name)
async def reg_t1(message:Message,state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer("Введите вашу фамилию:")
    await RegistrationTeacher.next()

@dp.message_handler(state=RegistrationTeacher.surname)
async def reg_t2(message:Message,state:FSMContext):
    surname = message.text
    await state.update_data(surname=surname)
    data = await state.get_data()
    await message.answer("Подтвердите или измените введённую вами информацию:")
    await message.answer(f"Имя: {data.get('name')}, Фамилия: {data.get('surname')}",reply_markup=accept_keyboard)
    await RegistrationTeacher.next()

@dp.message_handler(state=RegistrationTeacher.check)
async def reg_t3(message:Message,state:FSMContext):
    answer = message.text
    if answer == "Подтвердить":
        data = await state.get_data()
        name = data.get('name')
        surname = data.get('surname')
        teacher_id = message.from_user.id
        if name.isalpha() and surname.isalpha():
            try:
                db.add_new_teacher(teacher_id,name,surname)
                await message.answer("Вы успешно зарегистрировались!☺")
            except:
                await message.answer("Вы уже зарегистрированы")
        else:
            await message.answer("Вы ввели неверные данные")
    elif answer == "Изменить данные":
        await message.answer("Введите ваше имя:")
        await RegistrationTeacher.name.set()
        return
    await state.finish()

@dp.message_handler(commands=['tcourse'],state=None)
async def t_join_course_begin(message:Message):
    await message.answer("Администратором какого курса вы хотите стать? ",reply_markup=course_keyboard)
    await TeacherInCourse.coruse_name.set()

@dp.message_handler(state=TeacherInCourse.coruse_name)
async def t_join_coruse1(message:Message, state:FSMContext):
    course_name = message.text
    await state.update_data(course_name=course_name)
    await message.answer("Введите пароль от курса:",reply_markup=ReplyKeyboardRemove)
    await TeacherInCourse.next()

@dp.message_handler(state=TeacherInCourse.password)
async def t_join_course2(message:Message, state:FSMContext):
    password = message.text
    data = await state.get_data()
    course_name = data.get("course_name")
    try:
        if db.check_course_password(course_name,password):
            db.teacher_join_course(message.from_user.id,db.get_id_course_by_name(course_name))
            await message.answer(f"Вы стали администратором курса {course_name}")
        else:
            await message.answer("Вы ввели неверный пароль\nПопробуйте ещё раз")
    except:
        await message.answer("Что-то пошло не так...")
    await state.finish()


@dp.message_handler(commands=['getjournal'],state=None)
async def get_journal_begin(message: Message):
    await message.reply("Выберите предмет, по которому вы хотите получить журнал", reply_markup=course_keyboard)
    await GetJournal.journal.set()

@dp.message_handler(state=GetJournal.journal)
async def get_journal1(message: Message, state: FSMContext):
    course_name = message.text
    try:
        tid=message.from_user.id
        cid=db.get_id_course_by_name(course_name)
        if (db.course_check(tid,cid)):
            list_of_students = db.get_list_of_students(cid)
            n=len(list_of_students)
            journal=db.get_from_journal(cid)
            dates=[]
            hometasks=[]
            for i in journal:
                dates.append(i[2])
                hometasks.append(i[5])
            df = pd.DataFrame(columns = dates)
            df['Студент']=list_of_students
            i=0
            for student in list_of_students:
                df.loc[i]=db.get_grades(student[0],cid)
                i+=1
            df.loc[i]=hometasks
            df.insert(loc=0, column='Студенты', value=list_of_students)
            answer=df
            answer.to_excel(r"Журнал.xlsx")
            await message.answer
        else:
            await message.answer("Вы выбрали неправильный курс")
    except:
        await message.answer('Произошла непредвиденная ошибка')

@dp.message_handler(commands=['fillgrades'],state=None)
async def fill_grades(message: Message):
    await message.reply("Напишите дату выставления оценок в формате ДД.ММ.ГГГГ")
    await FillGrades.fill.set()

@dp.message_handler(state=FillGrades.fill)
async def fill_grades1(message: Message, state: FSMContext):
    try:
        answer = message.text
        df = pd.read_excel(r"Журнал.xlsx")
        grades = []
        for i in df[answer]:
            grades.append(i)
        cid = db.get_cid_by_tid(message.from_user.id)
        list_of_students = db.get_list_of_students(cid)
        for i in range(0, len(list_of_students)):
            try:
                if math.isnan(grades[i]):
                    db.assign_grades(list_of_students[i][0], cid, 0)
                else:
                    db.assign_grades(list_of_students[i][0], cid, grades[i])
            except:
                pass
        await message.answer('Оценки выставлены!')
    except:
        await message.answer('Не удалось найти файл с оценками')



@dp.message_handler(commands=['getattendencejournal'],state=None)
async def journal_attendece(message: Message):
    await message.reply("Выберите предмет, по которому вы хотите получить журнал посещаемости", reply_markup=course_keyboard)
    await GetAttendenceJournal.journal.set()

@dp.message_handler(state=GetAttendenceJournal.journal)
async def answer_q1(message: Message, state: FSMContext):
    course_name = message.text
    try:
        tid=message.from_user.id
        cid=db.get_id_course_by_name(course_name)
        if (db.course_check(tid,cid)):
            list_of_students = db.get_list_of_students(cid)
            n=len(list_of_students)
            journal=db.get_from_journal(cid)
            dates=[]
            for i in journal:
                dates.append(i[2])
            df = pd.DataFrame(columns = dates)
            df['Студент']=list_of_students
            i=0
            for student in list_of_students:
                df.loc[i]=db.get_attendence(student[0],cid)
                i+=1
            df.insert(loc=0, column='Студенты', value=list_of_students)
            answer=df
            answer.to_excel(r"Журнал_Посещаемости.xlsx")
            await message.answer
        else:
            await message.answer("Вы выбрали неправильный курс")
    except:
        await message.answer('Произошла непредвиденная ошибка')

@dp.message_handler(commands=['fillattendence'])
async def fill_gradse(message: Message):
    await message.reply("Напишите дату выставления посещаемости в формате ГГГГ-ММ-ДД")
    await FillAttendence.fill.set()

@dp.message_handler(state=FillAttendence.fill)
async def fill_grades1(message: Message, state: FSMContext):
    try:
        answer = message.text
        df = pd.read_excel(r"Журнал_Посещаемости.xlsx")
        attendence = []
        for i in df[answer]:
            attendence.append(i)
        cid = db.get_cid_by_tid(message.from_user.id)
        list_of_students = db.get_list_of_students(cid)
        for i in range(0, len(list_of_students)):
            try:
                db.assign_attendence(list_of_students[i][0], cid, attendence[i])
            except:
                pass
        await message.answer('Посещаемость выставлена!')
    except:
        await message.answer('Не удалось найти файл с оценками')


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




