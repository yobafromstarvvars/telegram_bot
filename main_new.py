import telebot
from telebot import types
from telebot import util
import pprint
import requests
import json

bot = telebot.TeleBot('5022795028:AAExr3GHbc-RohYgPtOs6jBYDfiFsVnYv8Y')

'''
send message
    text
    video
    image
    the same content that is sent by user (echoer)
    audio
    file
    sticker
    with timer
reply to message
    reply with text
    with photo, video
    with audio
    with file
forward message
handler filters
    filter by content type
        text
        video
        photo
    filter by chat type
        private chat
        private group
    filter by function
    and / or filters
style messages with HTML or Markdown
    how to make a new line
    how to reply to a message and style it
edit message
    text
    photo, video, file
delete message
    sender message
    send a message from bot and delete it right away
    any other message
inline keyboard
reply keyboard
buttons:
    url
    callback
    switch
callback
next_step_handler
    get user review about something
utils (message breaker, smart message breaker)
get user data
    review
    phone
quiz:
    max row width in reply keyboard
    max row width in inline keyboard
'''

bot.send_message('-1001921739828', 'Здравствуйте, меня зовут Administrator, я пришёл служить Вам.')

def get_chat_id():
    # Works with public channels only
    # testing chat id: -1001921739828
    return json.loads(requests.get('https://api.telegram.org/bot5022795028:AAExr3GHbc-RohYgPtOs6jBYDfiFsVnYv8Y/sendMessage?chat_id=@test1231241231&text=123').text)['result']['chat']['id']

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Логин', callback_data='login')
    btn4 = types.InlineKeyboardButton(text='Пополнить баланс', callback_data='replenish_account')
    btn2 = types.InlineKeyboardButton(text='Настройки', callback_data='settings')
    btn3 = types.InlineKeyboardButton(text='Оставить отзыв', callback_data='feedback')
    markup.add(btn1, btn4)
    markup.row(btn2, btn3)
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn_location = types.KeyboardButton(text='Получить местоположение', request_location=True)
    reply_markup.add(btn_location)
    bot.send_message(message.chat.id, text='Аккаунт: admin\nБаланс: 0₽', reply_markup=markup)


def get_code(message, messages_to_delete):
    bot.delete_messages(message.chat.id, messages_to_delete + [message.id])
    bot.send_message(message.chat.id, f'Номер подтверждён, вход выполнен')



def get_login(message, messages_to_delete):
    print(f"Login: {message.text}")
    if message.content_type == 'contact':
        # Debugging. Print the message
        # for chunk in util.smart_split(str(vars(message)), 3000):
        #     bot.send_message(message.chat.id, pprint.pformat(chunk))

        if message.contact.user_id == message.from_user.id:
            ask_confirm_code = bot.send_message(message.chat.id, f'На номер {message.contact.phone_number} выслан код подтверждения. Напишите код.')
            messages_to_delete.append(ask_confirm_code.id)
            messages_to_delete.append(message.id)
            bot.register_next_step_handler(ask_confirm_code, get_code, messages_to_delete)
        else:
            bot.send_message(message.chat.id, 'Вы не являетесь владельцем номера')

        # send code to phone number
        return
    # If login is not a number
    ask_password = bot.send_message(message.chat.id, 'Введите пароль')
    messages_to_delete.append(ask_password.id)
    messages_to_delete.append(message.id)
    bot.register_next_step_handler(ask_password, get_password, messages_to_delete)


def get_password(message, messages_to_delete):
    print(f"Password: {message.text}")
    messages_to_delete.append(message.id)
    print(messages_to_delete)
    bot.delete_messages(message.chat.id, messages_to_delete)
    bot.send_message(message.chat.id, 'Вход выполнен успешно')


def get_sum(message, request_message):
    print(f"Sum: {message.text}")
    bot.delete_message(message.chat.id, message)
    bot.edit_message_text(chat_id=request_message.chat.id, message_id=request_message.id, text=f"Аккаунт успешно пополнен на {message.text}₽")

@bot.message_handler(commands=['feedback'])
def feedback(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Сообщить об ошибке', callback_data='feedback_error')
    btn2 = types.InlineKeyboardButton(text='Предложить улучшения', callback_data='feedback_proposition')
    btn3 = types.InlineKeyboardButton(text='Поделиться', switch_inline_query='')
    btn4 = types.InlineKeyboardButton(text='Об авторе', url='https://en.wikipedia.org/wiki/Elon_Musk')
    markup.add(btn1, btn2, btn4, btn3)
    bot.send_message(message.chat.id, text='Выберите тему:', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'replenish_account')
def replenish_account_callback(callback):
    ask_sum = bot.send_message(callback.message.chat.id, 'Введите сумму для пополнения')
    bot.register_next_step_handler(ask_sum, get_sum, request_message=callback.message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'login')
def login(callback):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton(text='Использовать телефон ТГ', request_contact=True)
    btn2 = types.KeyboardButton(text='Использовать имя ТГ')
    btn3 = types.KeyboardButton(text='Использовать псевдоним ТГ')
    markup.row(btn1, btn2, btn3)
    ask_login = bot.send_message(chat_id=callback.message.chat.id, text='Введите логин', reply_markup=markup)
    bot.register_next_step_handler(callback.message, get_login, [ask_login.id, ])


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    markup = types.InlineKeyboardMarkup(row_width=1)
    match callback.data:
        case 'settings':
            pass
        case 'feedback':
            feedback(callback.message)
        case 'feedback_error':
            btn1 = types.InlineKeyboardButton(text='Мелкий баг', callback_data='small_bug')
            btn2 = types.InlineKeyboardButton(text='Не работает функционал или работает неверно', callback_data='big_bug')
            btn3 = types.InlineKeyboardButton(text='Другое', callback_data='other')
            markup.add(btn1, btn2, btn3)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id ,text='Укажите тип ошибки:', reply_markup=markup)
        case 'feedback_proposition':
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Напишите своё предложение:')
            bot.register_next_step_handler(callback.message, review)

def review(message):
    message_to_receive = message.text
    print(message_to_receive)
    # bot.delete_messages(message.chat.id, [message.id, ])
    bot.send_message(message.chat.id, 'Отзыв записан. Спасибо за обратную связь.')


# Handler for debugging. gm (get message)
# Examples:
# /gm - print message
# /gm-text - print message.text
# /gm-chat.first_name - print first_name
@bot.message_handler(commands=['gm'])
@bot.message_handler(regexp=r'gm-?.*')
@bot.message_handler(regexp=r'get message-?.*')
@bot.message_handler(regexp=r'msg-?.*')
@bot.message_handler(regexp=r'message-?.*')
def debug(message):
    # Delete user message, that called this command
    bot.delete_message(message.chat.id, message.id)

    if '-' in message.text:
        searched_var = message.text.split('-', 1)[1]
        attrs = searched_var.split('.')
        if hasattr(message, attrs[0]):
            var = getattr(message, attrs[0])
            for attr in attrs[1:]:
                try:
                    var = getattr(var, attr)
                except Exception as e:
                    bot.send_message(message.chat.id, e.__str__())
                    return
            bot.send_message(message.chat.id, var)
        else:
            bot.send_message(message.chat.id, f"'Message' object has no attribute '{attrs[0]}'")
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='msg')
        keyboard.add(btn1)
        bot.send_message(message.chat.id, pprint.pformat(vars(message)), reply_markup=keyboard)



bot.polling(non_stop=True)
