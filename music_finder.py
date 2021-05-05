from config import musixmatch_key
import requests

base_url = "https://api.musixmatch.com/ws/1.1/track.search?"
api_key = f"apikey={musixmatch_key}"
parameters = '&page_size=1&page=1&s_track_rating=desc'


def get_song(lyrics):
    lyrics = lyrics.replace(" ", "%20")
    q_lyrics = f'&q_lyrics={lyrics}'
    api_call = base_url + api_key + q_lyrics+parameters
    request = requests.get(api_call)
    data = request.json()
    tracks = data['message']['body']['track_list']
    if not(len(tracks)):
        return -1, -1
    track = tracks[0]['track']
    title = track['track_name']
    artist = track['artist_name']
    return title, artist
