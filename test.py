from imageai.Detection import ObjectDetection
import os
import telebot
import telegram
from telebot import apihelper
from telebot import types
import time
from os import path
import speech_recognition as sr


apihelper.proxy = {'https': 'https://51.158.68.68:8811'}

bot = telebot.TeleBot('TOKEN', threaded=False)

print('Бот запущен')
admins = ''
bot.send_message(admins, 'Бот запущен')

@bot.message_handler(content_types=['photo'])
def photo(message):
    bot.send_message(message.chat.id, 'Я начал работу. Пожалуйста, подождите')
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    print('Ky')
    execution_path = os.getcwd()
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.1.0.h5")) # Download the model via this link https://github.com/OlafenwaMoses/ImageAI/releases/tag/1.0
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "image.jpg"), output_image_path=os.path.join(execution_path , "detected.jpg"), minimum_percentage_probability=40)

    for eachObject in detections:
        print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
        print("--------------------------------")
        
    foto = open('/home/pi/Desktop/AIbot/detected.jpg', 'rb')
    bot.send_photo(message.chat.id, foto)
    os.remove('image.jpg')
    os.remove('detected.jpg')
    print('файлы удадены')
        
        
        
        
@bot.message_handler(content_types=['voice'])

        
while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=123)
    except Exception as E:
        print(E.args)
        time.sleep(2)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
