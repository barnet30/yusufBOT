import telebot

bot = telebot.TeleBot("1301833528:AAHzcF_MANvxQuzssdKLJfNbRJMHp1D8AJ4")


@bot.message_handler(commands=['start'])
def set_welcome(message):
    bot.reply_to(message, "Hi, how can i help you?")

@bot.message_handler(commands=['hello'])
def set_welcome(message):
    bot.reply_to(message, "Приветствую тебя в мире cars")

# @bot.message_handler(func= lambda x:True)
# def echo_all(message):
#     bot.reply_to(message,message.text)

@bot.message_handler(content_types=['text'])
def message_all(msg):
    message = msg.text
    user_id = msg.chat.id
    bot.send_message(user_id, f"Вы написали ахахах {message}")




bot.polling()
