class ServerNotWorkingError(Exception):
    pass


class YoutubeError(Exception):
    def __init__(
        self,
        code: int,
        message: str,
        details: dict,
    ):
        self.code = code
        self.message = message
        self.data = details

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.message}>"


class WrongResponseError(Exception):
    pass


class VideoNotFoundError(Exception):
    pass
