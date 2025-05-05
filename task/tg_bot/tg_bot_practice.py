import telebot

# Токен, полученный от BotFather
TOKEN = '7678787402:AAEbm8MwQlC0NWQufbHAneGddgt5XchoTR4'

# Создаём объект бота
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой бот. Напиши /help, чтобы узнать, что я умею.")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Я умею отвечать на команды /start и /help. Скоро научусь большему!")

# Запуск бота (polling)
bot.polling()