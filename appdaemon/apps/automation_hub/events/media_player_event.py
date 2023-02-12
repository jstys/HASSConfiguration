from dataclasses import dataclass

@dataclass
class MediaPlayerEvent:
    media_player_name: str
    state: str
    app_name: str
