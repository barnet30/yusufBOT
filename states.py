from aiogram.dispatcher.filters.state import State,StatesGroup

class RegistrationStudent(StatesGroup):
    name = State()
    surname = State()
    group = State()
    age = State()
    gradebook = State()

class StudInCourse(StatesGroup):
    s1 = State()

class StudLeaveCourse(StatesGroup):
    s1 = State()

class GetAverageValues(StatesGroup):
    s1 = State()

class GetWorstStudents(StatesGroup):
    s1 = State()

class GetCorrelation(StatesGroup):
    s1 = State()