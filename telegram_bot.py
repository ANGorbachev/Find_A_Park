import os
import cv2
import telebot
import webbrowser
from telebot import types
from calibration import calibration
from find_park import get_bboxes, get_available_parkings

bot = telebot.TeleBot('#TELEGRAM_API_TOKEN#')

def do_calibration():
    try:
        calibration()
        return 0
    except Exception as e:
        return 1

def get_parkings():
    try:
        dump = get_bboxes()
        available_parkings = get_available_parkings(dump)
        return available_parkings
    except FileNotFoundError:
        return 1
    except Exception as e:
        return 2

@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://cars.###############.ru/user/########/')


@bot.message_handler(commands=['start'])
def main(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Калибровка')
    btn2 = types.KeyboardButton('Найди парковку!')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id,
                     f'Hello {message.from_user.first_name} {message.from_user.last_name}! I am a Telegram Bot that can show you vacant auto parking place at home =)', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Калибровка':
        bot.reply_to(message, "Начинаем калибровку...")
        exitcode = do_calibration()
        if exitcode == 0:
            bot.send_message(message.chat.id, 'Calibration completed successfully')
        else:
            bot.send_message(message.chat.id, 'Error occurred during calibration! Try again later...')
    elif message.text == 'Найди парковку!':
        bot.reply_to(message, "Ищем парковочные места...")
        exitcode = get_parkings()
        if exitcode == 1:
            bot.send_message(message.chat.id, "Calibration file not found! Complete the calibration prior to find a parking")
        elif exitcode == 2:
            bot.send_message(message.chat.id, 'Runtime error...')
        else:
            try:
                for img in exitcode:
                    # cv2.imwrite('./temp/tmp.jpg', img)
                    # image_file = open('./temp/tmp.jpg', 'rb')
                    # bot.send_photo(message.chat.id, image_file)
                    # os.remove('./temp/tmp.jpg')
                    ret, img_encode = cv2.imencode('.jpg', img)
                    img_bytes = img_encode.tobytes()
                    # img_byteio = BytesIO(str_encode)
                    bot.send_photo(message.chat.id, img_bytes)

            except Exception as e:
                bot.send_message(message.chat.id, f'Runtime error during image fetching: {e}')


bot.polling(none_stop=True)

# bot.infinity_polling()
