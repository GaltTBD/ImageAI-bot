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

bot = telebot.TeleBot('1044896825:AAH6Ejkd8Ni-zOryBph6y5ozNR5-kNcLvY0', threaded=False)

print('Бот запущен')
admins = '726597187'
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
def photo(message):
    print('Voice')
    bot.send_message(message.chat.id, 'Я начал работу. Пожалуйста, подождите')
    fileID = message.voice.file_id
    file = bot.get_file(fileID)
    print ("file_id: " + str(fileID))
    #file.download('voice.ogg')
    downloaded_file = bot.download_file(file.file_path)
    with open("voice.wav", 'wb') as new_file:
        new_file.write(downloaded_file)
    #bot.register_next_step_handler(message, voice_send)

    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "voice.wav")
    r = sr.Recognizer()
    print('Начал преобразование')
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)
        print('Готово')
    try:
        text = r.recognize_google(audio)
        print(text)
        print('Отправил айдио')
        bot.send_message(admins, text)
    except:
        print('Ошибка')
        bot.send_message(admins, 'Ошибка... Попробуй еще раз')

    os.remove('voice.wav')
    print('Аудио удалено')
    
        
while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=123)
    except Exception as E:
        print(E.args)
        time.sleep(2)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)