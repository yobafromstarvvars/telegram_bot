import telebot

bot = telebot.TeleBot('5022795028:AAExr3GHbc-RohYgPtOs6jBYDfiFsVnYv8Y')

@bot.message_handler(commands=['dick'])
def main(message):
    bot.reply_to(message, 'hello world')

bot.polling()

