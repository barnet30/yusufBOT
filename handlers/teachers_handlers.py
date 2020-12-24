from main import db
from loader import dp, bot
from aiogram.types import Message, ReplyKeyboardRemove, ContentType
from states import GetAverageValues, GetWorstStudents, GetCorrelation, RegistrationTeacher, \
    TeacherInCourse, GetJournal, GetAttendenceJournal, FillGrades, FillAttendence,    DeleteGrades,UpdateAttendence,ChangeGrades
from aiogram.dispatcher import FSMContext
from keybords_button import course_keyboard, accept_keyboard
import pandas as pd
import math
import traceback
import numpy as np


@dp.message_handler(commands=['reg_teacher'], state=None)
async def reg_teacher_begin(message: Message):
    await message.answer("Введите ваше имя:")
    await RegistrationTeacher.name.set()


@dp.message_handler(state=RegistrationTeacher.name)
async def reg_t1(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer("Введите вашу фамилию:")
    await RegistrationTeacher.next()


@dp.message_handler(state=RegistrationTeacher.surname)
async def reg_t2(message: Message, state: FSMContext):
    surname = message.text
    await state.update_data(surname=surname)
    data = await state.get_data()
    await message.answer("Подтвердите или измените введённую вами информацию:")
    await message.answer(f"Имя: {data.get('name')}, Фамилия: {data.get('surname')}", reply_markup=accept_keyboard)
    await RegistrationTeacher.next()


@dp.message_handler(state=RegistrationTeacher.check)
async def reg_t3(message: Message, state: FSMContext):
    answer = message.text
    if answer == "Подтвердить":
        data = await state.get_data()
        name = data.get('name')
        surname = data.get('surname')
        teacher_id = message.from_user.id
        if name.isalpha() and surname.isalpha():
            try:
                db.add_new_teacher(teacher_id, name, surname)
                await message.answer("Вы успешно зарегистрировались!☺", reply_markup=ReplyKeyboardRemove())
            except:
                await message.answer("Вы уже зарегистрированы", reply_markup=ReplyKeyboardRemove())
                return
        else:
            await message.answer("Вы ввели неверные данные", reply_markup=ReplyKeyboardRemove())
    elif answer == "Изменить данные":
        await message.answer("Введите ваше имя:")
        await RegistrationTeacher.name.set()
        return
    await state.finish()


@dp.message_handler(commands=['tcourse'], state=None)
async def t_join_course_begin(message: Message):
    await message.answer("Администратором какого курса вы хотите стать? ", reply_markup=course_keyboard)
    await TeacherInCourse.coruse_name.set()


@dp.message_handler(state=TeacherInCourse.coruse_name)
async def t_join_coruse1(message: Message, state: FSMContext):
    course_name = message.text
    await state.update_data(course_name=course_name)
    await message.answer("Введите пароль от курса:", reply_markup=ReplyKeyboardRemove())
    await TeacherInCourse.next()


@dp.message_handler(state=TeacherInCourse.password)
async def t_join_course2(message: Message, state: FSMContext):
    password = message.text
    data = await state.get_data()
    course_name = data.get("course_name")
    try:
        if db.check_course_password(course_name, password):
            db.teacher_join_course(message.from_user.id, db.get_id_course_by_name(course_name))
            await message.answer(f"Вы стали администратором курса {course_name}")
        else:
            await message.answer("Вы ввели неверный пароль\nПопробуйте ещё раз")
    except:
        await message.answer("Что-то пошло не так...")
    await state.finish()


@dp.message_handler(commands=['getaveragevalues'], state=None)
async def enter_course_stats(message: Message):
    await message.reply("Выберите предмет, по которому Вы хотите получить средние показатели",
                        reply_markup=course_keyboard)
    await GetAverageValues.s1.set()


@dp.message_handler(state=GetAverageValues.s1)
async def answer_q1(message: Message, state: FSMContext):
    try:
        answer = message.text
        cid = db.get_id_course_by_name(answer)
        list_of_students = db.get_list_of_students(cid)
        n = len(list_of_students)
        grades_sum = 0
        ages_sum = 0
        couples_sum = 0
        fin_couples = 0
        for student in list_of_students:
            stud_couple=0
            grades_sum += sum(db.get_grades(student[0], cid))
            ages_sum += db.get_age(student[0])
            for couple in db.get_attendence(student[0], cid):
                if couple == "Н" or couple == "У":
                    pass
                else:
                    couples_sum += 1
                    stud_couple +=1
            fin_couples = max(fin_couples,stud_couple)
        if n == 0:
            await message.answer("Нет студентов на данном курсе")
        elif fin_couples == 0:
            await message.answer("Занятий ещё не проводилось" +
                                 "Средний возраст студентов: " +
                                 str(ages_sum / n))
        else:
            await message.answer("Средний балл за курс: " +
                                 str(grades_sum / n) +
                                 "\nСредняя посещаемость: " +
                                 str(couples_sum / (n * fin_couples) * 100) + "%" +
                                 "\nСредний возраст студентов: " +
                                 str(ages_sum / n))
    except:
        await message.answer("Произошла непредвиденная ошибка")
    await state.finish()


@dp.message_handler(commands=['getworststudents'], state=None)
async def get_top5(message: Message):
    await message.reply(
        "Выберите предмет, по которому Вы хотите полученить данные о студентах, у которых не хватает баллов до зачёта",
        reply_markup=course_keyboard)
    await GetWorstStudents.s1.set()


@dp.message_handler(state=GetWorstStudents.s1)
async def answer_q1(message: Message, state: FSMContext):
    try:
        answer = message.text
        cid = db.get_id_course_by_name(answer)
        list_of_students = db.get_list_of_students(cid)
        worst_students = ""
        for student in list_of_students:
            if sum(db.get_grades(student[0], cid)) < 56:
                worst_students = worst_students + f"{student[1]} {student[2]} : {sum(db.get_grades(student[0], cid))}\n"
        if len(list_of_students) == 0:
            await message.answer("Нет студентов на данном курсе", reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(worst_students, reply_markup=ReplyKeyboardRemove())
    except:
        await message.answer("Произошла непредвиденная ошибка", reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(commands=['getcorrelation'], state=None)
async def course_corr_begin(message: Message):
    await message.reply("Выберите предмет, по которому Вы хотите получить корреляционную зависимость",
                        reply_markup=course_keyboard)
    await GetCorrelation.s1.set()


@dp.message_handler(state=GetCorrelation.s1)
async def course_corr1(message: Message, state: FSMContext):
    try:
        answer = message.text
        cid = db.get_id_course_by_name(answer)
        list_of_students = db.get_list_of_students(cid)
        n = len(list_of_students)
        grades_list = []
        attendence_list = []
        ages_list = []
        couples_list = []
        for student in list_of_students:
            grades_list.append(sum(db.get_grades(student[0], cid)))
            couples_list = db.get_attendence(student[0], cid)
            couples_sum = 0
            ages_list.append(db.get_age(student[0]))
            for couple in couples_list:
                if couple == "Н" or couple == "У":
                    pass
                else:
                    couples_sum += 1
            attendence_list.append(couples_sum)

        grades_list = pd.Series(grades_list)
        attendence_list = pd.Series(attendence_list)
        ages_list = pd.Series(ages_list)
        if n == 0:
            await message.answer("Нет студентов на данном курсе", reply_markup=ReplyKeyboardRemove())
        elif len(couples_list) == 0:
            await message.answer("Занятий ещё не проводилось", reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer("Коэффециент корреляции между оценками и посещаемость: " +
                                 str(grades_list.corr(attendence_list)) +
                                 "Коэффециент корреляции между оценками и возрастом: " +
                                 str(grades_list.corr(ages_list)) +
                                 "Коэффециент корреляции между посещаемостью и возрастом: " +
                                 str(attendence_list.corr(ages_list)), reply_markup=ReplyKeyboardRemove())
    except:
        await message.answer("Произошла непредвиденная ошибка", reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(commands=['getjournal'])
async def get_journal(message: Message):
    try:
        tid=message.from_user.id
        cid=db.get_cid_by_tid(tid)
        students = db.get_list_of_students(cid)
        journal=db.get_from_journal(cid)
        dates=[]
        names=[]
        surnames=[]
        groups=[]
        zach_books =[]
        grades = []
        check = False
        for i in journal:
            dates.append(i[2])
        for student in students:
            grades_stud =[]
            names.append(student[1])
            surnames.append(student[2])
            groups.append(student[4])
            zach_books.append(student[3])
            for j in db.get_grades(student[0],cid):
                grades_stud.append(j)
            grades.append(grades_stud)
            if grades_stud:
                check = True
        amounts_grades=[]
        for g in grades:
            amounts_grades.append(len(g))
        df = pd.DataFrame({'Фамилия': surnames, 'Имя': names, 'Группа': groups, 'Номер зачётной книжки': zach_books})
        if check:
            max_amount_grades = max(amounts_grades)
            dates = list(set(dates))
            dates.sort()
            for grade in grades:
                if len(grade) < max_amount_grades:
                    while len(grade) < max_amount_grades:
                        grade.insert(len(grade), 0)
            df_grades = pd.DataFrame(columns=dates)
            #print(len(grades),len(df_grades),len(df_grades.columns))
            j = 0
            #print(grades)
            for col in df_grades.columns:
                g =[]
                for i in range(len(students)):
                    g.append(grades[i][j])
                df_grades[col] = np.array(g)
                #print(col)
                j+=1
            answer = pd.merge(df,df_grades,left_index=True,right_index=True)
            answer.to_excel(r"Журнал.xlsx")

        else:
            answer = df
            answer.to_excel(r"Журнал.xlsx")
        await message.answer(f"Журнал для курса {db.get_name_course_by_id(cid)}",reply_markup=ReplyKeyboardRemove())
        with open("Журнал.xlsx",'rb') as file:
            await dp.bot.send_document(message.from_user.id, file)
    except:
        await message.answer('Вы не являетесь администратором ни одного из курсов',reply_markup=ReplyKeyboardRemove())
        print(traceback.format_exc())
        return

@dp.message_handler(commands=['fillgrades'],state=None)
async def fill_grades_begin(message:Message):
    await message.answer("Прикрепите файл 'Журнал.xlsx' к своему сообщению")
    await FillGrades.fill.set()

@dp.message_handler(state=FillGrades.fill, content_types=ContentType.DOCUMENT)
async def fill_grades1(message: Message, state: FSMContext):
    try:
        file_info = await bot.get_file(message.document.file_id)
        journal = await bot.download_file(file_info.file_path)
        src = 'C:/Users/barnet/PycharmProjects/yusufBOT'+message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(journal)
        df = pd.read_excel(r"Журнал.xlsx")
        del df['Фамилия']
        del df['Имя']
        del df['Группа']
        del df['Номер зачётной книжки']
        for date in df.columns:
            grades = []
            for i in df[date]:
                grades.append(i)
            cid = db.get_cid_by_tid(message.from_user.id)
            list_of_students = db.get_list_of_students(cid)
            for i in range(0, len(list_of_students)):
                try:
                    if math.isnan(grades[i]):
                        db.assign_grades(list_of_students[i][0], cid, date, 0)
                    else:
                        db.assign_grades(list_of_students[i][0], cid, date, grades[i])
                except:
                    pass
        await message.answer('Оценки выставлены!')
    except:
        await message.answer('Не удалось найти файл с оценками')
        print(traceback.format_exc())

@dp.message_handler(commands=['changegrades'])
async def change_grades(message: Message):
    await message.reply("Напишите дату оценок, подлежащих изменению, в формате ГГГГ-ММ-ДД")
    await ChangeGrades.change.set()
                         
@dp.message_handler(state=FillGrades.fill)
async def change_grades1(message: Message, state: FSMContext):
    try:
        cid = db.get_cid_by_tid(message.from_user.id)
        list_of_students = db.get_list_of_students(cid)
        answer = message.text
        for student in list_of_students:
            db.add_couple(student[0],cid,answer)
        df = pd.read_excel(r"Оценки.xlsx")     
        grades = []
        for grade in df[answer]:
            if math.isnan(grade):
                grades.append(0)
            else:
                grades.append(int(grade))
        for i in range(0, len(list_of_students)):
            try:
                db.assign_grades(list_of_students[i][0], cid, answer, grades[i])
            except:
                pass
        await message.answer('Оценки выставлены!')
    except:
        await message.answer('Не удалось найти файл с оценками')
    await state.finish()  

@dp.message_handler(commands=['deletegrades'])
async def delete_gradse(message: Message):
    await message.reply("Напишите оценки за какую дату вы хотели бы удалить (в формате ГГГГ-ММ-ДД)")
    await DeleteGrades.delete.set()
                         
@dp.message_handler(state=DeleteGrades.delete)
async def delete_grades1(message: Message, state: FSMContext):
    try:
        cid = db.get_cid_by_tid(message.from_user.id)
        answer = message.text
        db.delete_grades(cid,answer)
        await message.answer('Оценки удалены!')
    except:
        await message.answer('Не удалось удалить оценки')
    await state.finish()         


@dp.message_handler(commands=['getattendencejournal'])
async def get_attendence_journal(message: Message):
    try:
        tid=message.from_user.id
        cid=db.get_cid_by_tid(tid)
        students = db.get_list_of_students(cid)
        journal=db.get_from_journal(cid)
        dates=[]
        names=[]
        surnames=[]
        groups=[]
        zach_books =[]
        attendence = []
        check = False
        for i in journal:
            dates.append(i[2])
        for student in students:
            attendence_stud =[]
            names.append(student[1])
            surnames.append(student[2])
            groups.append(student[4])
            zach_books.append(student[3])
            for j in db.get_attendece(student[0],cid):
                attendence_stud.append(j)
            attendence.append(attendence_stud)
            if attendence_stud:
                check = True
        amounts_attendence=[]
        for a in attendence:
            amounts_attendence.append(len(a))
        df = pd.DataFrame({'Фамилия': surnames, 'Имя': names, 'Группа': groups, 'Номер зачётной книжки': zach_books})
        if check:
            max_amount_attendence = max(amounts_attendence)
            dates = list(set(dates))
            dates.sort()
            for a in attendence:
                if len(a) < max_amount_attendence:
                    while len(a) < max_amount_attendence:
                        a.insert(len(a), 0)
            df_attendence = pd.DataFrame(columns=dates)
            #print(len(grades),len(df_grades),len(df_grades.columns))
            j = 0
            #print(grades)
            for col in df_attendence.columns:
                at =[]
                for i in range(len(students)):
                    at.append(attendence[i][j])
                df_attendence[col] = np.array(at)
                #print(col)
                j+=1
            answer = pd.merge(df,df_attendence,left_index=True,right_index=True)
            answer.to_excel(r"Журнал_Посещаемости.xlsx")

        else:
            answer = df
            answer.to_excel(r"Журнал_Посещаемости.xlsx")
        await message.answer(f"Журнал посещаемости для курса {db.get_name_course_by_id(cid)}",reply_markup=ReplyKeyboardRemove())
        with open("Журнал_Посещаемости.xlsx",'rb') as file:
            await dp.bot.send_document(message.from_user.id, file)
    except:
        await message.answer('Вы не являетесь администратором ни одного из курсов',reply_markup=ReplyKeyboardRemove())
        print(traceback.format_exc())
        return


@dp.message_handler(commands=['updateattendence'])
async def update_attendence(message: Message):
    await message.reply("Напишите дату выставления посещаемости в формате ГГГГ-ММ-ДД\nУбедитесь, что вы выставили оценки за эту дату")
    await UpdateAttendence.fill.set()

@dp.message_handler(state=UpdateAttendence.fill)
async def update_attendence1(message: Message, state: FSMContext):
    try:
        cid = db.get_cid_by_tid(message.from_user.id)
        list_of_students = db.get_list_of_students(cid)
        answer = message.text
        df = pd.read_excel(r"Посещаемость.xlsx")     
        attendence = []
        for i in df[answer]:
            if math.isnan(i):
                attendence.append(" ")
            else:
                attendence.append(i)
        for i in range(0, len(list_of_students)):
            try:
                db.assign_attendence1(list_of_students[i][0], cid, answer, attendence[i])
            except:
                pass
        await message.answer('Посещаемость выставлена!')
    except:
        await message.answer('Не удалось найти файл с посещаемостью')
    await state.finish() 
