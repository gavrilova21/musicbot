from bs4 import BeautifulSoup
import requests
from errors import NotFoundYandexMusicException

start_page = "https://music.yandex.ru"


class ParserYandexMusic:
    page_pattern = "https://music.yandex.ru/search?text="

    def __init__(self, title, artist):
        title = title.replace(" ", "%20")
        title = title.lower()
        self.title = title

        artist = artist.replace(" ", "%20")
        artist = artist.lower()
        self.artist = artist
        self.link = self.page_pattern + self.artist + "%20" + self.title

    def parse(self):
        soup = BeautifulSoup(requests.get(self.link).content, "html.parser")
        schedule = soup.find_all(class_="d-track__name")
        return schedule


def get_ref(title, artist):
    parser = ParserYandexMusic(title=title, artist=artist)
    array_of_songs = parser.parse()
    if len(array_of_songs) == 0:
        raise NotFoundYandexMusicException(title, artist)
    else:
        song = array_of_songs[0]
        song = str(song)
        start = song.find("/album")
        ref = song[start:].split('\"')[0]

        return start_page + ref
