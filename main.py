import telebot
from config import keys, TOKEN, currency_ex
from extensions import ConvertionException, CriptoConverter


bot = telebot.TeleBot(TOKEN)


def auto_mode():
    sp_c = []
    for key in keys.keys():
        sp_c.append(str(keys[key]))
    return sp_c

@bot.message_handler(commands=['start','help'])
def echo_test(message: telebot.types.Message):
    currency_ex.clear()
    text = ('Выберите тип работы БОТа \
            \n/manual - ручной ввод данных \
            \n /auto - автоматический')
    bot.reply_to(message, text)

@bot.message_handler(commands=['manual'])
def manual_text(message: telebot.types.Message):
    text = ('Поставьте запрос Боту в формате: \n<название валюты> \
        <в какую валюту перевести> \
        <количество переводимой валюты> \
        \n Для вывода списка доступных валют наберите команду: /values')
    bot.reply_to(message,text)

@bot.message_handler(commands=['auto'])
def auto_text(message: telebot.types.Message):
    currency_ex.clear()
    text = ('Выберите валюту:')
    for key in keys.keys():
        str_k = str(f'{key} - /{keys[key]}')
        text = '\n'.join((text, str_k, ))
    bot.reply_to(message,text)

@bot.message_handler(commands=auto_mode())
def auto_text_2(message: telebot.types.Message):
    if len(currency_ex) == 0:
        currency_ex.append(message.text[1::])
        text = ('Выберите в какую валюту перевести:')
        for key in keys.keys():
            str_k = str(f'{key} - /{keys[key]}')
            text = '\n'.join((text, str_k,))
        bot.reply_to(message, text)
    elif len(currency_ex) == 1:
        currency_ex.append(message.text[1::])
        text = 'Введите колличество: '
        bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        if len(currency_ex) > 0:
            amount = float(message.text)
            quote = str([key for key in keys if keys[key] == currency_ex[0]])[2:-2:]
            base = str([key for key in keys if keys[key] == currency_ex[1]])[2:-2:]
            currency_ex.clear()

        else:
            values = message.text.split(' ')

            if len(values) != 3:
                raise ConvertionException('Некорректный запрос, уточните данные /help')

            quote, base, amount = values

        total_base = CriptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {float(total_base)*float(amount)}'
        bot.send_message(message.chat.id, text)

bot.polling()