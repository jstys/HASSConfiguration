from util.entity_map import name_map
from util.entity_map import entity_map
from util import hassutil
from util import logger

class MediaPlayerAction():
    def __init__(self):
        self._media_players = []

    def add_media_players(self, media_players):
        for media_player in media_players:
            self.add_media_player(media_player)

        return self

    def add_media_player(self, media_player):
        if media_player in name_map:
            self._media_players.append(hassutil.Entity(name_map[media_player]))
        else:
            logger.error("Unable to add unknown light to MediaPlayerAction: {}".format(media_player))

        return self

    def turn_on(self):
        for media_player in self._media_players:
            hassutil.turn_on(media_player)

    def turn_off(self):
        for media_player in self._media_players:
            hassutil.turn_off(media_player)
            
    def pause(self):
        for media_player in self._media_players:
            hassutil.call_service("media_player", "pause", entity_id=media_player)
        
    def play(self):
        for media_player in self._media_players:
            hassutil.call_service("media_player", "play", entity_id=media_player)
            
    def change_input(self, input_name):
        for media_player in self._media_players:
            inputs = entity_map.get(media_player.entity_id).get("inputs")
            if input_name in inputs:
                hassutil.call_service("media_player", "select_source", entity_id=media_player, source=inputs.get(input_name))
            else:
                logger.error("Unable to set {} input on {}".format(media_player, input_name))
            
            
    def mute(self):
        for media_player in self._media_players:
            hassutil.call_service("media_player", "volume_mute", entity_id=media_player, is_volume_muted=True)
            
    def unmute(self):
        for media_player in self._media_players:
            hassutil.call_service("media_player", "volume_mute", entity_id=media_player, is_volume_muted=False)