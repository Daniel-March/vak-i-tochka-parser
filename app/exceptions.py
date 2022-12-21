class DefaultException(Exception):
    def __init__(self, text: str):
        self.__text = text

    @property
    def text(self):
        return self.__text


class ConfigPathError(DefaultException):
    pass


class FilesError(DefaultException):
    pass


class InternetError(DefaultException):
    pass
