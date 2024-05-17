from telebot import types
from telebot import util
import time
import telebot
import pprint

bot = telebot.TeleBot('5022795028:AAExr3GHbc-RohYgPtOs6jBYDfiFsVnYv8Y')


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton(text='/del')
    btn2 = types.KeyboardButton(text='/edit')
    btn3 = types.KeyboardButton(text='/inline')
    btn4 = types.KeyboardButton(text='/start')
    btn5 = types.KeyboardButton(text='Получить телефон', request_contact=True)
    keyboard.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, 'Hello', reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def get_contact(message):
    if message.from_user.id == message.contact.user_id:
        bot.send_message(message.chat.id, message.contact.phone_number)
    else:
        bot.send_message(message.chat.id, 'not your number')
    # bot.send_message(message.chat.id, pprint.pformat(vars(message)))


@bot.callback_query_handler(func=lambda callback: callback.data == 'break_string')
def break_long_string(callback):
    long_string = 'Dick was a Mongolian noblewoman and the mother of Temüjin, better known as Genghis Khan. She played a major role in his rise to power.'
    for chunk in util.smart_split(long_string, 20):  # The maximum length of a Telegram message is 4096 characters
        bot.send_message(callback.message.chat.id, chunk)


@bot.callback_query_handler(func=lambda callback: callback.data == 'home')
@bot.message_handler(commands=['inline'])
def print_inline_keyboard(message_or_callback):
    # If callback => retrieve message
    message = message_or_callback if type(message_or_callback) is not types.CallbackQuery else message_or_callback.message
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='text, url', url='google.com')
    btn2 = types.InlineKeyboardButton(text='text, switch_inline_query', switch_inline_query='- это многофункциональный телеграмм бот для вашего расписания')
    btn3 = types.InlineKeyboardButton(text='text, callback_data', callback_data='btn1')
    btn4 = types.InlineKeyboardButton(text='text, callback_data, break_string', callback_data='break_string')
    btn5 = types.InlineKeyboardButton(text='review', callback_data='get_review')
    btn6 = types.InlineKeyboardButton(text='get callback text', callback_data='get_callback_text')
    keyboard.row(btn1, btn2)
    keyboard.add(btn3)
    keyboard.row(btn4, btn5, btn6)
    bot.send_message(message.chat.id, 'InlineKeyboardMarkup', reply_markup=keyboard)





@bot.callback_query_handler(func=lambda callback: callback.data == 'get_callback_text')
def get_callback_text(callback):
    bot.send_message(callback.message.chat.id, pprint.pformat(vars(callback)))


def process_review(message):
    print(message.text)

@bot.callback_query_handler(func=lambda callback: callback.data == 'get_review')
def get_review(callback):
    bot_message = bot.send_message(callback.message.chat.id, 'Type in review:')
    bot.register_next_step_handler(bot_message, process_review)

@bot.callback_query_handler(func=lambda callback: callback.data and callback.data == 'btn1', )
def callback_handler(callback):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='go back', callback_data='home')
    keyboard.add(btn1)
    bot.send_message(callback.message.chat.id, callback)
    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='callback changed keyboard text', reply_markup=keyboard)

@bot.message_handler(content_types=['photo'])
def reply_photo(message):
    bot.send_photo(message.chat.id, message.photo[0].file_id, reply_to_message_id=message.id)


@bot.message_handler(commands=['del'])
def delete_message(message):
    bot.delete_message(message.chat.id, message.id)


@bot.message_handler(commands=['edit'])
def edit_message(message):
    bot_message = bot.send_message(message.chat.id, 'original message')
    time.sleep(1)
    bot.edit_message_text(chat_id=message.chat.id, message_id=bot_message.id, text='Hello World')


@bot.message_handler(commands=['echo'])
@bot.message_handler(content_types=['text'])
def reply_text(message):
    # bot.reply_to(message, f'*{message.text}*')
    bot.send_message(message.chat.id, f'<i>{message.text}</i>\nreply_text()', parse_mode='HTML', reply_to_message_id=message.id)





bot.polling()

