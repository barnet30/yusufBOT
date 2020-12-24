from aiogram.dispatcher.filters.state import State,StatesGroup

class RegistrationStudent(StatesGroup):
    name = State()
    surname = State()
    group = State()
    age = State()
    gradebook = State()
    check = State()

class StudInCourse(StatesGroup):
    s1 = State()

class StudLeaveCourse(StatesGroup):
    s1 = State()

###
class GetOverall(StatesGroup):
    s1 = State()
###
###
class GetGrades(StatesGroup):
    s1 = State()
###

class GetAverageValues(StatesGroup):
    s1 = State()

class GetWorstStudents(StatesGroup):
    s1 = State()

class GetCorrelation(StatesGroup):
    s1 = State()

class RegistrationTeacher(StatesGroup):
    name = State()
    surname = State()
    check = State()

class TeacherInCourse(StatesGroup):
    coruse_name = State()
    password = State()

class GetJournal(StatesGroup):
    journal = State()

class FillGrades(StatesGroup):
    fill = State()

class GetAttendenceJournal(StatesGroup):
    journal = State()

class FillAttendence(StatesGroup):
    fill = State()

class DeleteGrades(StatesGroup):
    delete = State()

class UpdateAttendence(StatesGroup):
    fill = State()

class ChangeGrades(StatesGroup):
    change = State()
