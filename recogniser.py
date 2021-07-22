from acrcloud.recognizer import ACRCloudRecognizer
from config import ACRCLOUD_KEY, ACRCLOUD_SECRET
from dataclasses import dataclass

config = {
    'host': 'eu-west-1.api.acrcloud.com',
    'access_key': ACRCLOUD_KEY,
    'access_secret': ACRCLOUD_SECRET,
    'timeout': 10  # seconds
}


@dataclass
class Track:
    title: str
    artist: str


def cleaned_response(name):
    return ''.join(list(filter(lambda ch: ch not in "?.!/;:\\\"'{[]}", name)))


def get_response(music_file_path, start_seconds=3):
    recognizer = ACRCloudRecognizer(config)
    response = recognizer.recognize_by_file(file_path=music_file_path, start_seconds=start_seconds)
    return response


def get_parsed_responses(response):
    responses = []
    for response_element in response.split(':'):
        responses += response_element.split(',')
    return responses


def success_recognise_track(responses):
    found = True

    for i, response_element in enumerate(responses):
        if 'msg' in response_element:
            if 'Success' in responses[i + 1]:
                print('Start processing')
                break
            else:
                print("Not found")
                found = False
                break
    return found


def get_track_info(responses):
    title = None
    artist = None

    for i, response_element in enumerate(responses):
        if 'title' in response_element:
            title = cleaned_response(responses[i + 1])

        if 'artists' in response_element and 'name' in responses[i + 1]:
            artist = cleaned_response(responses[i + 2])

    return Track(title, artist)


def parse_response(response):
    responses = get_parsed_responses(response)

    if success_recognise_track(responses):
        return get_track_info(responses)

    return Track(None, None)
