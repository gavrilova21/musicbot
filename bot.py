import telebot
import config
import recogniser
import yandex_parsing
import messages
from music_finder import get_song

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
def sound_listener(message):
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
            bot.send_message(message.chat.id, messages.NOT_FOUND_MESSAGE)
        else:
            yandex_music_link = yandex_parsing.get_ref(title, artist)
            if yandex_music_link == -1:  # если песня нашлась, но ее нет в Я.Музыке
                result_message = messages.SUCCESS_FOUND.format(title, artist)
            else:
                result_message = f"Нашел 😄\nЭто же песня \"{title}\" исполнителя {artist}!\n" + \
                                 f"Можешь послушать ее на Яндекс.Музыке {yandex_music_link} "
            bot.send_message(message.chat.id, result_message)


@bot.message_handler(content_types=["text"])
def text_recogniser(message):
    title, artist = get_song(message.text)
    if title == -1:
        bot.send_message(message.chat.id, messages.NOT_FOUND_MESSAGE)
    else:
        yandex_music_link = yandex_parsing.get_ref(title, artist)
        if yandex_music_link == -1:  # если песня нашлась, но ее нет в Я.Музыке
            result_message = messages.SUCCESS_FOUND.format(title, artist)
        else:
            result_message = f"Нашел 😄\nЭто же песня \"{title}\" исполнителя {artist}!\n" + \
                             f"Можешь послушать ее на Яндекс.Музыке {yandex_music_link} "
        bot.send_message(message.chat.id, result_message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
