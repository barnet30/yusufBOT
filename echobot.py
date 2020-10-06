import telebot

bot = telebot.TeleBot("1301833528:AAHzcF_MANvxQuzssdKLJfNbRJMHp1D8AJ4", parse_mode=None)
user = bot.get_me()


@bot.message_handler(commands=['start','help'])
def set_welcome(message):
    bot.reply_to(message, "Bros, how are you?")

@bot.message_handler(func= lambda x:True)
def echo_all(message):
    bot.reply_to(message,message.text)

@bot.callback_query_handler(func= lambda x:True)
def test_callback(call):
    user.info(call)

bot.polling()
