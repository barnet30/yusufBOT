from aiogram.dispatcher.filters.state import State,StatesGroup

class RegistrationStudent(StatesGroup):
    s1 = State()
    s2 = State()
    s3 = State()
    s4 = State()
    s5 = State()

class StudInCourse(StatesGroup):
    s1 = State()