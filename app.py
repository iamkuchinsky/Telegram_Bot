import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_cd(message: telebot.types.Message):
    text = ('Привет! Это бот-обменник валют\nВведите команду в формате:\nДоллар рубль 100'
            '\nРезультатом будет стоимость 100 долларов в рублях\n/values - список всех доступных'
            ' валют\n/help - помощь')
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help_cd(message: telebot.types.Message):
    text = ('Чтобы начать работу введите команду в следующем формате(через пробел):\n<имя валюты, цену которой '
            'хотите узнать>  <имя валюты, в которой надо узнать цену первой валюты>  <количество первой '
            'валюты>\n/values - список всех доступных валют\n/start - начальная страница')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values_cd(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Проверьте корректность и Повторите ввод команды.\n/help - помощь')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Неправильный ввод команды:\n{e}')
    else:
        text = f'Переводим {quote} в {base}\n{amount} {quote} = {float(total_base) * float(amount)} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
