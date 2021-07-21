from acrcloud.recognizer import ACRCloudRecognizer
from config import ACRCLOUD_KEY, ACRCLOUD_SECRET

config = {
    'host': 'eu-west-1.api.acrcloud.com',
    'access_key': ACRCLOUD_KEY,
    'access_secret': ACRCLOUD_SECRET,
    'timeout': 10  # seconds
}


def get_response(music_file_path, start_seconds=3):
    recognizer = ACRCloudRecognizer(config)
    response = recognizer.recognize_by_file(file_path=music_file_path, start_seconds=start_seconds)
    return response


def parse_response(response):
    response_splitted = response.split(':')
    responses = []
    for i, response_element in enumerate(response_splitted):
        responses += response_element.split(',')

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

    title = None
    artist = None

    if found:
        for i, response_element in enumerate(responses):
            if 'title' in response_element:
                title = responses[i + 1]
                title = ''.join(
                    list(
                        filter(
                            lambda ch: ch not in "?.!/;:\\\"'{[]}", title)
                    )
                )
            if 'artists' in response_element and 'name' in responses[i + 1]:
                artist = responses[i + 2]
                artist = ''.join(
                    list(
                        filter(
                            lambda ch: ch not in "?.!/;:\\\"'{[]}", artist)
                    )
                )

    return title, artist
