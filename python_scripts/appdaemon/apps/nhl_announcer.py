#!/srv/homeassistant/bin/python3
import appdaemon.appapi as appapi

class NHLAnnouncer(appapi.AppDaemon):
    def __init__(self, name, logger, error, args, global_vars):
        pass

    def initialize(self):
        self.listen_event(self.on_period_start, "nhl_period_start")
        self.listen_event(self.on_period_end, "nhl_period_end")
        self.listen_event(self.on_goal, "nhl_goal")
        self.listen_event(self.on_penalty, "nhl_penalty")
        self.listen_event(self.on_game_end, "nhl_game_end")

    def on_period_start(self, event, data, kwargs):
        pass

    def on_period_end(self, event, data, kwargs):
        pass

    def on_goal(self, event, data, kwargs):
        pass

    def on_penalty(self, event, data, kwargs):
        pass

    def on_game_end(self, event, data, kwargs):
        pass
