import telebot
import config
import recogniser
import yandex_parsing
import messages
import os
from music_finder import get_song
from flask import Flask, request

server = Flask(__name__)

# config.py - все токены

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(message, messages.HELLO)


@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.reply_to(message, messages.HELP)


# декоратор, если приходит голосовое сообщение или аудио
@bot.message_handler(content_types=["voice", "audio"])
def listener(message):
    try:
        file_id = message.voice.file_id
    except AttributeError:
        file_id = message.audio.file_id

    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    downloaded_audio = bot.download_file(file_path)

    audio_file = config.audio_dir

    with open(audio_file, "wb") as new_file:
        new_file.write(downloaded_audio)
        response = recogniser.get_response(music_file_path=config.audio_dir,
                                           start_seconds=3)

        title, artist = recogniser.parse_response(response)

        if not (title and artist):
            result_message = "К сожалению, я не нашел такую песню ("
            bot.send_message(message.chat.id, result_message)
        else:
            yandex_music_link = yandex_parsing.get_ref(title, artist)
            if yandex_music_link == -1:  # если песня нашлась, но ее нет в Я.Музыке
                result_message = f"Нашел 😄\nЭто же песня \"{title}\" исполнителя {artist}!\n"
            else:
                result_message = f"Нашел 😄\nЭто же песня \"{title}\" исполнителя {artist}!\n" + \
                                 f"Можешь послушать ее на Яндекс.Музыке {yandex_music_link} "
            bot.send_message(message.chat.id, result_message)


@bot.message_handler(content_types=["text"])
def listener(message):
    title, artist = get_song(message.text)
    if title == -1:
        bot.send_message(message.chat.id, "К сожалению, я не нашел такую песню (")
    else:
        yandex_music_link = yandex_parsing.get_ref(title, artist)
        if yandex_music_link == -1:  # если песня нашлась, но ее нет в Я.Музыке
            result_message = f"Нашел 😄\nЭто же песня \"{title}\" исполнителя {artist}!\n"
        else:
            result_message = f"Нашел 😄\nЭто же песня \"{title}\" исполнителя {artist}!\n" + \
                             f"Можешь послушать ее на Яндекс.Музыке {yandex_music_link} "
        bot.send_message(message.chat.id, result_message)


@server.route('/' + config.token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://quiet-bayou-54355.herokuapp.com/' + config.token)
    return "!", 200


if __name__ == '__main__':
    server.debug = True
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    bot.polling(none_stop=True)
