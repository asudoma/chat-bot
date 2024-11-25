import re


def check_youtube_id(text: str) -> bool:
    youtube_regex = (
        r"^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|"
        r"youtube\.com/embed/|youtube\.com/v/)([a-zA-Z0-9_-]{11})"
    )
    return bool(re.match(youtube_regex, text))
