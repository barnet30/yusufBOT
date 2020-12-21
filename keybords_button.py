from aiogram.types import KeyboardButton,ReplyKeyboardMarkup

course1 = KeyboardButton('Python🐍')
course2 = KeyboardButton('C#')
course3 = KeyboardButton('Java')
course4 = KeyboardButton('Database design')
course5 = KeyboardButton('Methods of optimizations')

course_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
course_keyboard.row(course1, course2, course3)
course_keyboard.add(course4, course5)

accept_button = KeyboardButton("Подтвердить")
change_button = KeyboardButton("Изменить данные")
accept_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
accept_keyboard.add(accept_button,change_button)

yes_button = KeyboardButton("Да")
no_button = KeyboardButton("Нет")
choice_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
choice_keyboard.add(yes_button,no_button)

