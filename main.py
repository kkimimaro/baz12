import os

from flask import Flask, request
from telebot import types

import telebot
import qrcode
from telebot import types
from gtts import gTTS

TOKEN = '5286040884:AAGJ5Qx-2uc4tu0mCJ9ewN4cWdRoWQptbTg'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start']) 
def start(message):
  keyboard = types.ReplyKeyboardMarkup()
  keyboard.add("qr код")
  keyboard.add("аудио")
  bot.send_message(message.chat.id, 'тмукг', reply_markup= keyboard)
  bot.register_next_step_handler(message, make)

def make(message):
  if message.text=="аудио":
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add("mp3")
    keyboard.add("голосовое сообщение")
    bot.send_message(message.chat.id, 'выбирете, как отправить аудио', reply_markup= keyboard)
    bot.register_next_step_handler(message, audiochoice)
  if message.text=="qr код":
    bot.send_message(message.chat.id, 'введите текст для qr кода')
    bot.register_next_step_handler(message, qrtext)
  
def audiochoice(message):
  if message.text=="mp3":
    bot.register_next_step_handler(message, makeaudio_mp3)
  if message.text=="голосовое сообщение":
    bot.register_next_step_handler(message, makeaudio_voise)


def qrtext(message):
  qrcodetext = message.text  #message.text забирает текст, который ввел пользователь  нужна отдельная ветка
  image = qrcode.make(qrcodetext)
  image.save('qr.png')
  img = open('qr.png','rb')
  bot.send_photo(message.from_user.id, img)
  img.close()

def makeaudio_mp3(message):
  bot.send_message(message.chat.id, 'введите текст для создания аудио файла')
  bot.register_next_step_handler(message, audiotextmp3)

def audiotextmp3(message):
  audiotext = message.text  #message.text забирает текст, который ввел пользователь  нужна отдельная ветка
  audio = gTTS(audiotext, lang= 'ru')
  audio.save('audio.mp3')
  aud = open('audio.mp3','rb')
  bot.send_audio(message.from_user.id, aud)
  aud.close()

def makeaudio_voise(message):
  bot.send_message(message.chat.id, 'введите текст для создания аудио файла')
  bot.register_next_step_handler(message, audiotextvoice)

def audiotextvoice(message):
  audiotext = message.text  #message.text забирает текст, который ввел пользователь  нужна отдельная ветка
  audio = gTTS(audiotext, lang= 'ru')
  audio.save('audio.mp3')
  aud = open('audio.mp3','rb')
  bot.send_voice(message.from_user.id, aud)
  aud.close()
  
  
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200
    
@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://bazzzz.herokuapp.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
