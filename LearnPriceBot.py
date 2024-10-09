import telebot
import cryptocompare


bot = telebot.TeleBot('')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Привет {message.from_user.first_name}, введи тикер крипты, например - BTC ")


@bot.message_handler(content_types=['text'])
def send_text(message):
    print(f'{message.text} ---from({message.from_user.first_name})')
    coin = message.text.upper()
    all_available_coins = cryptocompare.get_coin_list(format=True)
    if coin in all_available_coins:
        try:
            price = cryptocompare.get_price(coin, currency="USD").get(coin).get("USD")

            if "e" in str(price):
                bot.send_message(message.chat.id, f'{coin}\n{str(f"{price:.13f}").rstrip("0")}')
            else:
                bot.send_message(message.chat.id, f'{coin}\n{price}$')

        except AttributeError:
            bot.send_message(message.chat.id, "Такого токена нет или нет информации о нем")
    else:
        bot.send_message(message.chat.id, "Такого токена нет или нет информации о нем")


bot.polling(none_stop=True)



