from aiogram.types import KeyboardButton,ReplyKeyboardMarkup

btn1 = KeyboardButton('Python🐍')
btn2 = KeyboardButton('C#')
btn3 = KeyboardButton('Java')
btn4 = KeyboardButton('Database design')
btn5 = KeyboardButton('Methods of optimizations')

btn_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_markup.row(btn1, btn2, btn3)
btn_markup.add(btn4,btn5)

btny = KeyboardButton("Подтвердить")
btnn = KeyboardButton("Изменить данные")
btn_accept = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_accept.add(btny,btnn)

