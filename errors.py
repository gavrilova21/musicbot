class NotFoundYandexMusicException(Exception):
    """Исключение если трек не найден в Я Музыке"""

    def __init__(self, title, artist):
        self.message = f'Не найден трэк {artist} - {title}'


class NotFoundMusicxException(Exception):
    """Исключение если трек не найден в Musix"""
    pass
