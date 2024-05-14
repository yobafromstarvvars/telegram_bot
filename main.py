import telebot

bot = telebot.TeleBot('5022795028:AAExr3GHbc-RohYgPtOs6jBYDfiFsVnYv8Y')

def f(message):
    if message.text == '1':
        return True
    else:
        return False


@bot.message_handler(chat_types=['supergroup'], func=f)
def main(message):
    bot.reply_to(message, message.chat.type)

@bot.message_handler(commands=['get_photo'])
def get_photo(message):
    file = open('photo_2023-12-27_13-51-18.jpg', 'rb')
    bot.send_photo(message.chat.id, file, "I don't know how to solve this, HELP")

@bot.message_handler(content_types=['photo'])
def resend_photo(message):
    bot.send_photo(message.chat.id, message.photo[0].file_id)


bot.polling(none_stop=True)


