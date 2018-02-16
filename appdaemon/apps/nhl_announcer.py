#!/srv/homeassistant/bin/python3
import appdaemon.appapi as appapi
from hassutil import tts_say, tts_broadcast, call_service

class NHLAnnouncer(appapi.AppDaemon):
    def __init__(self, name, logger, error, args, global_vars):
        super().__init__(name, logger, error, args, global_vars)

        # TODO: make more configurable
        self.team = "New Jersey Devils"

    def initialize(self):
        self.listen_event(self.on_period_start, "nhl_period_start")
        self.listen_event(self.on_period_end, "nhl_period_end")
        self.listen_event(self.on_goal, "nhl_scoring")
        self.listen_event(self.on_penalty, "nhl_penalty")
        self.listen_event(self.on_game_end, "nhl_game_end")

    def on_period_start(self, event, data, kwargs):
        tts_broadcast(self, "Start of {}".format(self._get_period_num(data.get('period'))))

    def on_period_end(self, event, data, kwargs):
        tts_broadcast(self, "End of {}".format(self._get_period_num(data.get('period'))))

    def on_goal(self, event, data, kwargs):
        team = data.get('team')
        scorer = data.get('scorer')
        scorer_number = scorer.get('number')
        scorer_name = scorer.get('name')
        assists = data.get('assists')
        tts_message = "{} goal scored by number {}, {}.".format(team, scorer_number, scorer_name)
        if assists:
            tts_message += " Assisted by"
            for assist_player in assists:
                tts_message += " number {}, {}".format(assist_player.get('number'), assist_player.get('name'))

        if team == self.team:
            call_service(self, "script", "rick_flair_woo")

        tts_broadcast(self, tts_message)

    def on_penalty(self, event, data, kwargs):
        team = data.get('team')
        player = data.get('player')
        player_number = player.get('number')
        player_name = player.get('name')
        penalty = data.get('description')
        tts_broadcast(self, "{} penalty on number {}, {}. {}".format(team, player_number, player_name, penalty))

    def on_game_end(self, event, data, kwargs):
        tts_broadcast(self, "The devils game has ended")

    def _get_period_num(self, num):
        if num == 1:
            return "the 1st period"
        elif num == 2:
            return "the 2nd period"
        elif num == 3:
            return "the 3rd period"
        elif num > 3:
            return "Overtime"

