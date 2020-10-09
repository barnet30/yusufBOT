import echobot as eb
import user

def main():
    eb.bot.polling()
    user.User.get_all_id()

if __name__ == '__main__':
    main()