from main import db
from loader import dp
from aiogram.types import Message,ReplyKeyboardRemove
from states import GetAverageValues, GetWorstStudents, GetCorrelation, RegistrationTeacher,\
    TeacherInCourse, GetJournal,GetAttendenceJournal,FillGrades,FillAttendence
from aiogram.dispatcher import FSMContext
from keybords_button import course_keyboard, accept_keyboard
import pandas as pd
import math
import traceback


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
                await message.answer("Вы успешно зарегистрировались!☺",reply_markup=ReplyKeyboardRemove())
            except:
                await message.answer("Вы уже зарегистрированы",reply_markup=ReplyKeyboardRemove())
                return
        else:
            await message.answer("Вы ввели неверные данные",reply_markup=ReplyKeyboardRemove())
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
    await message.answer("Введите пароль от курса:",reply_markup=ReplyKeyboardRemove())
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
    except Exception as err:
        await message.answer('Произошла непредвиденная ошибка')
        await message.answer(traceback.format_exc())
    await state.finish()

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
    await state.finish()



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
    await state.finish()

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
    await state.finish()

