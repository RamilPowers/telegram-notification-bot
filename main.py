import threading
import telebot
from settings import key

bot = telebot.TeleBot(key)
users = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        f'Привет, {str(message.chat.first_name)}!\n\n'
        'Я сделаю для тебя заметку и вовремя оповещу тебя о ней 😉\n'
        'Все просто: сначала напиши о чем тебе напомнить и следующим сообщением через сколько минут.\n\n'
        'Погнали? Напиши заметку'
    )


@bot.message_handler(content_types=['text'])
def get_message(message):
    alert = message.text
    chat_id = message.chat.id
    answer = f'Понял, {str(message.chat.first_name)}.\n Сообщение: {str(message.text)}.\n Через сколько минут напомнить?'
    bot.send_message(message.chat.id, text=answer)
    bot.register_next_step_handler(message, get_time)
    users[chat_id] = [alert]


def get_time(message):
    timelaps = message.text
    chat_id = message.chat.id
    alert = users[chat_id][0]
    users[chat_id].insert(1, timelaps)
    
    def check_in():
        bot.send_message(message.chat.id, text=f'НАПОМИНАЮ: {alert}') 

    while not timelaps.isdigit():
        bot.send_message(message.chat.id, 'Цифрами, пожалуйста 😉')
        bot.register_next_step_handler(message, get_time)
        users[chat_id].pop() 
        break    
    else:
        bot.send_message(message.chat.id, 'Ok')
        t = threading.Timer(int(timelaps)*60, check_in)
        t.start()


bot.polling(none_stop=True, timeout=20)
