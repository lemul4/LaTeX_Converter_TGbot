import telebot
from Converter import converter 


bot = telebot.TeleBot('6199288836:AAEDRijGj-InSLA3tPiheFrr7f3cxyyPiqc')

value = ""
old_value = ""

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
    global value
    match message.text:
        case "/start":
            bot.send_message(message.chat.id, "Привет, это LaTeX Tranlator bot, который поможет тебе перевести любую математическую формулу в LaTeX формат. Чтобы ознакомиться с инструментарием бота введите команду /help")
        case "/help":
            bot.send_message(message.chat.id, "Доступно 3 вида ввода: через клавиатуру, через кнопки /buttons, с фотографии (отправить фотографию).")
        case "/buttons":
            if value == "":
                bot.send_message(message.chat.id, "!", reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, value, reply_markup=keyboard)
        case _:
            bot.send_message(message.chat.id, converter(message.text))


@bot.message_handler(content_types=["photo"])
def get_photo(image):
    photo = open("Srek.jpg", 'rb')
    bot.send_photo(image.chat.id, photo)
    

@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global value, old_value 
    cursorIndex = value.find("!")
    data = query.data
    match data:
        case "C":
            value = ""
        case "=":
            value = converter(value.replace('!',""))
        case "←":
            if value != "":
                value = value[:value.find("!")-1] + value[value.find("!"):]
        case "<":
            value = value[:cursorIndex-1] + "!" + value[cursorIndex-1] + value[cursorIndex+1:]
        case ">":
            value = value[:cursorIndex] + value[cursorIndex+1] + "!" + value[cursorIndex+2:]
        case _:
            if value == "!" or value == "":
                value = data + "!"
            else:
                value = value[:value.find("!")] + data + "!" + value[value.find("!")+1:] 
                  
    if (value != old_value and value != "") or ("!" != old_value and value == ""):
        if value == "":
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                  text="!", reply_markup=keyboard)
            old_value = "!"
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                  text=value, reply_markup=keyboard)
     
    old_value = value
    
bot.polling(none_stop=True)