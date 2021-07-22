from config import MUSIXMATCH_KEY
import requests
from errors import NotFoundMusicxException

BASE_URL = "https://api.musixmatch.com/ws/1.1/track.search?"
API_KEY = f"apikey={MUSIXMATCH_KEY}"
PARAMETERS = '&page_size=1&page=1&s_track_rating=desc'


def get_song(lyrics):
    lyrics = lyrics.replace(" ", "%20")
    q_lyrics = f'&q_lyrics={lyrics}'
    api_call = BASE_URL + API_KEY + q_lyrics + PARAMETERS
    request = requests.get(api_call)
    data = request.json()
    tracks = data['message']['body']['track_list']
    if not(len(tracks)):
        raise NotFoundMusicxException
    track = tracks[0]['track']
    title = track['track_name']
    artist = track['artist_name']
    return title, artist
