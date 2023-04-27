import telebot
import sqlite3
from Converter import converter


bot = telebot.TeleBot('6199288836:AAEDRijGj-InSLA3tPiheFrr7f3cxyyPiqc')

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(telebot.types.InlineKeyboardButton('(', callback_data='('),
             telebot.types.InlineKeyboardButton(')', callback_data=')'),
             telebot.types.InlineKeyboardButton('C', callback_data='C'),
             telebot.types.InlineKeyboardButton('←', callback_data='←'))

keyboard.row(telebot.types.InlineKeyboardButton('tg', callback_data='tg()'),
             telebot.types.InlineKeyboardButton('cot', callback_data='cot()'),
             telebot.types.InlineKeyboardButton('sin', callback_data='sin()'),
             telebot.types.InlineKeyboardButton('cos', callback_data='cos()'))

keyboard.row(telebot.types.InlineKeyboardButton('ln', callback_data='ln()'),
             telebot.types.InlineKeyboardButton('√', callback_data='sqrt()'),
             telebot.types.InlineKeyboardButton('^', callback_data='^()'),
             telebot.types.InlineKeyboardButton('∞', callback_data='∞'))

keyboard.row(telebot.types.InlineKeyboardButton('e', callback_data='e'),
             telebot.types.InlineKeyboardButton('π', callback_data='pi'),
             telebot.types.InlineKeyboardButton('<', callback_data='<'),
             telebot.types.InlineKeyboardButton('>', callback_data='>'))

keyboard.row(telebot.types.InlineKeyboardButton('7', callback_data='7'),
             telebot.types.InlineKeyboardButton('8', callback_data='8'),
             telebot.types.InlineKeyboardButton('9', callback_data='9'),
             telebot.types.InlineKeyboardButton('/', callback_data='/'))

keyboard.row(telebot.types.InlineKeyboardButton('4', callback_data='4'),
             telebot.types.InlineKeyboardButton('5', callback_data='5'),
             telebot.types.InlineKeyboardButton('6', callback_data='6'),
             telebot.types.InlineKeyboardButton('×', callback_data='*'))

keyboard.row(telebot.types.InlineKeyboardButton('1', callback_data='1'),
             telebot.types.InlineKeyboardButton('2', callback_data='2'),
             telebot.types.InlineKeyboardButton('3', callback_data='3'),
             telebot.types.InlineKeyboardButton('-', callback_data='-'))

keyboard.row(telebot.types.InlineKeyboardButton(',', callback_data='.'),
             telebot.types.InlineKeyboardButton('0', callback_data='0'),
             telebot.types.InlineKeyboardButton('=', callback_data='='),
             telebot.types.InlineKeyboardButton('+', callback_data='+'))


@bot.message_handler(content_types=["text"])
def get_text(message):
    match message.text:
        case "/start":
            bot.send_message(
                message.chat.id, "Привет, это LaTeX Tranlator bot, который поможет тебе перевести любую математическую формулу в LaTeX формат. Чтобы ознакомиться с инструментарием бота введите команду /help")

        case "/help":
            bot.send_message(message.chat.id, """Ввод вручную (текстовым сообщением):
    Аргумент любой функции (за исключением ln с простым аргументом) должен выделяться скобками
        Примеры: cos(3) или sin((3)/(2)) или ln(e+4), но ln5
    Каждый элемент операции деления или дроби должен выделяться скобками
        Примеры: (3)/(5)
    Как вводить другие операции:
        Умножение => "*" [Например: 5*4]
        Бесконечность (+/-) => "inf" [Например: -inf]
        Число пи => "pi" [Например: pi*5]
        Умножение => "*" [Например: 5*4
        Экспонента => "e" [Например :e*9]
        Степень => "^" , показатель степени выделять скобками [Например: e^(5)]
        Корень квадратный m => "sqrt(m)" [Например: sqrt(4) - квадратный корень четырех]
        Корень m n-ой степени => "sqrt[n](m)" [Например: sqrt[3](4) - кубический корень четырёх]

Ввод кнопками:
    Вызов кнопок => "/buttons"
    "!" - курсор
    "<" и ">" - перемещение курсора
    Требования ввода не отличаются от ввода вручную

Фото от Шрека - отправить любую фотографию""")

        case "/buttons":
            database = sqlite3.connect("user_values.sql")
            cur = database.cursor()

            cur.execute(
                'CREATE TABLE IF NOT EXISTS users (chat_id int primary key, message_id int, new_value varchar(50))')
            database.commit()

            cur.execute('REPLACE INTO users (chat_id, message_id, new_value) VALUES ("%s", "%s", "!")' % (
                message.chat.id, message.message_id))
            database.commit()
            cur.close()
            database.close()

            bot.send_message(message.chat.id, "!", reply_markup=keyboard)

        case _:
            bot.send_message(message.chat.id, converter(message.text))


@bot.message_handler(content_types=["photo"])
def get_photo(image):
    photo = open("Srek.jpg", 'rb')
    bot.send_photo(image.chat.id, photo)


@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    n_value = "!"

    database = sqlite3.connect("user_values.sql")
    cur = database.cursor()
    values = cur.execute(
        "SELECT new_value FROM users WHERE chat_id='%s' " % (query.message.chat.id))

    for row in values:
        n_value = row[0]

    o_value = n_value
    cursorIndex = n_value.find("!")
    data = query.data

    match data:
        case "C":
            n_value = "!"

        case "=":
            n_value = converter(n_value.replace('!', ""))

        case "←":
            if len(n_value) > 1 and n_value[0] != "!":
                n_value = n_value[:n_value.find(
                    "!")-1] + n_value[n_value.find("!"):]

        case "<":
            if cursorIndex != 0:
                n_value = n_value[:cursorIndex-1] + "!" + \
                    n_value[cursorIndex-1] + n_value[cursorIndex+1:]

        case ">":
            if cursorIndex < (len(n_value)-1):
                n_value = n_value[:cursorIndex] + \
                    n_value[cursorIndex+1] + "!" + n_value[cursorIndex+2:]

        case _:
            if n_value == "!" or n_value == "":
                n_value = data + "!"
            else:
                n_value = n_value[:n_value.find(
                    "!")] + data + "!" + n_value[n_value.find("!")+1:]

    if n_value != o_value:
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                              text=n_value, reply_markup=keyboard)

    cur.execute("UPDATE users set new_value = '%s' WHERE chat_id = '%s'" %
                (n_value, query.message.chat.id))
    database.commit()
    cursor = cur.execute('SELECT * FROM users')
    for row in cursor:
        print(row)
    cur.close()
    database.close()


bot.polling(none_stop=True)
