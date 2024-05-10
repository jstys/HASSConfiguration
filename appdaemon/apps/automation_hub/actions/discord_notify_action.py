from util import hassutil
from util.entity_map import join_targets

CHANNEL_IDS = {
    "general": "1237199111229276233"
}

class DiscordNotifyAction():
    def __init__(self):
        self._targets = []
        self._message = None
        self._title = None
        self._kwargs = {}
        
    def add_channels(self, *channels):
        for channel in channels:
            self.add_channel(channel)
        
        return self
        
    def add_channel(self, channel):
        if channel in CHANNEL_IDS:
            self._targets.append(CHANNEL_IDS[channel])
        
        return self
            
    def set_message(self, message, title="Home Assistant", **kwargs):
        self._message = message
        self._title = title
        self._kwargs = kwargs
        return self

    def notify(self):
        hassutil.discord_notify(self._targets, self._message, title=self._title, data=self._kwargs)